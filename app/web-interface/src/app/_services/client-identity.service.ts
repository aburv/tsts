import { Injectable } from '@angular/core';

interface ClientSession {
    clientToken: string;
    expiresAt: number;
}

@Injectable({ providedIn: 'root' })
export class ClientIdentityService {
    private readonly platform = 'web';
    private readonly databaseName = 'takbuff-client-identity';
    private readonly storeName = 'keys';
    private readonly installationStorageKey = 'takbuff.installation.id';
    private readonly tokenStorageKey = 'takbuff.client.token';
    private readonly expiryStorageKey = 'takbuff.client.expiry';
    private pendingToken?: Promise<string>;

    getToken(): Promise<string> {
        if (!this.pendingToken) {
            this.pendingToken = this.loadOrCreateToken().finally(() => {
                this.pendingToken = undefined;
            });
        }
        return this.pendingToken;
    }

    private async loadOrCreateToken(): Promise<string> {
        const token = localStorage.getItem(this.tokenStorageKey);
        const expiry = Number(localStorage.getItem(this.expiryStorageKey) || 0);
        if (token && expiry > Math.floor(Date.now() / 1000) + 60) {
            return token;
        }

        const installationId = this.getInstallationId();
        const keyPair = await this.getKeyPair();
        const publicKey = encodeBase64(await crypto.subtle.exportKey('spki', keyPair.publicKey));
        const challengeResponse = await fetch('/api/client/challenge', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ data: { installationId, publicKey, platform: this.platform } })
        });
        if (!challengeResponse.ok) {
            throw new Error(`Client challenge failed: ${challengeResponse.status}`);
        }
        const challenge = (await challengeResponse.json()).data.challenge as string;
        const rawSignature = await crypto.subtle.sign(
            { name: 'ECDSA', hash: 'SHA-256' },
            keyPair.privateKey,
            new TextEncoder().encode(challenge)
        );
        const signature = encodeBase64(rawSignatureToDer(new Uint8Array(rawSignature)));
        const sessionResponse = await fetch('/api/client/session', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ data: { installationId, platform: this.platform, challenge, signature } })
        });
        if (!sessionResponse.ok) {
            throw new Error(`Client session failed: ${sessionResponse.status}`);
        }
        const session = (await sessionResponse.json()).data as ClientSession;
        localStorage.setItem(this.tokenStorageKey, session.clientToken);
        localStorage.setItem(this.expiryStorageKey, String(session.expiresAt));
        return session.clientToken;
    }

    private getInstallationId(): string {
        let value = localStorage.getItem(this.installationStorageKey);
        if (!value) {
            value = crypto.randomUUID().replaceAll('-', '');
            localStorage.setItem(this.installationStorageKey, value);
        }
        return value;
    }

    private async getKeyPair(): Promise<CryptoKeyPair> {
        const database = await this.openDatabase();
        const stored = await new Promise<CryptoKeyPair | undefined>((resolve, reject) => {
            const request = database.transaction(this.storeName, 'readonly')
                .objectStore(this.storeName).get('client-key-pair');
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
        if (stored) return stored;

        const keyPair = await crypto.subtle.generateKey(
            { name: 'ECDSA', namedCurve: 'P-256' },
            false,
            ['sign', 'verify']
        ) as CryptoKeyPair;
        await new Promise<void>((resolve, reject) => {
            const request = database.transaction(this.storeName, 'readwrite')
                .objectStore(this.storeName).put(keyPair, 'client-key-pair');
            request.onsuccess = () => resolve();
            request.onerror = () => reject(request.error);
        });
        return keyPair;
    }

    async getRequestHeaders(method: string, url: string, body: string | null): Promise<Record<string, string>> {
        const token = await this.getToken();
        const keyPair = await this.getKeyPair();
        const timestamp = String(Math.floor(Date.now() / 1000));
        const requestId = crypto.randomUUID();
        const bodyHash = await sha256Hex(body || '');
        const installationId = this.getInstallationId();
        const path = new URL(url, window.location.origin).pathname;
        const canonical = [method.toUpperCase(), path, timestamp, requestId, bodyHash,
            this.platform, installationId].join('\n');
        const rawSignature = await crypto.subtle.sign(
            { name: 'ECDSA', hash: 'SHA-256' }, keyPair.privateKey,
            new TextEncoder().encode(canonical)
        );
        return {
            'x-api-key': `Client ${token}`,
            'X-Client-Installation': installationId,
            'X-Client-Platform': this.platform,
            'X-Client-Timestamp': timestamp,
            'X-Client-Request-Id': requestId,
            'X-Client-Signature': encodeBase64(rawSignatureToDer(new Uint8Array(rawSignature)))
        };
    }

    private openDatabase(): Promise<IDBDatabase> {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this.databaseName, 1);
            request.onupgradeneeded = () => request.result.createObjectStore(this.storeName);
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }
}

async function sha256Hex(value: string): Promise<string> {
    const hash = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(value));
    return Array.from(new Uint8Array(hash), byte => byte.toString(16).padStart(2, '0')).join('');
}

function encodeBase64(value: ArrayBuffer | Uint8Array): string {
    const bytes = value instanceof Uint8Array ? value : new Uint8Array(value);
    let binary = '';
    bytes.forEach(byte => binary += String.fromCharCode(byte));
    return btoa(binary);
}

function rawSignatureToDer(signature: Uint8Array): Uint8Array {
    const half = signature.length / 2;
    const encodeInteger = (value: Uint8Array): number[] => {
        let first = 0;
        while (first < value.length - 1 && value[first] === 0) first++;
        const bytes = Array.from(value.slice(first));
        if (bytes[0] & 0x80) bytes.unshift(0);
        return [0x02, bytes.length, ...bytes];
    };
    const r = encodeInteger(signature.slice(0, half));
    const s = encodeInteger(signature.slice(half));
    const body = [...r, ...s];
    return new Uint8Array([0x30, body.length, ...body]);
}
