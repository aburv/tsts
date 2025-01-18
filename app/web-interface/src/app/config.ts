import { environment } from '../environments/environment';

export class Config {
    static getEnv(): any {
        return environment;
    }

    static getApiProtocol(): string {
        return this.getEnv().production ? 'https' : 'http';
    }

    static getDomain(): string {
        return this.getApiProtocol() + '://' + this.getEnv().domain + '/api/';
    }

    static getSiteDomain(): string {
        return this.getApiProtocol() + '://' + this.getEnv().siteDomain;
    }

    static getHeaders(): any {
        return {
            headers: {
                'x-api-key': this.getEnv().key,
                'content-type': 'application/json'
            }
        };
    }
}