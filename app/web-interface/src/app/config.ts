import { environment } from '../environments/environment';
import { LocalDataService } from './_services/localStore.service';

export class Config {
    static getEnv(): any {
        return environment;
    }
    static getDomain(): string {
        return '/api/';
    }

    static getSiteDomain(): string {
        return this.getEnv().siteDomain;
    }

    static getHeaders(): any {
        const data = new LocalDataService(this.getEnv().authKey).getValues();
        return {
            headers: {
                'x-api-key': this.getEnv().key,
                'content-type': 'application/json',
                'x-access-key': data !== null ? data['idToken'] + this.getEnv().separator + data['accessToken'] : ""
            }
        };
    }

    static getGCID(): string {
        return this.getEnv().googleServiceAccount;
    }
}
