import { environment } from '../environments/environment';

export class Config {
    static getEnv(): any{
        return environment;
    }

    static getDomain(): string {
        return this.getEnv().protocol + '://' + this.getEnv().domain + '/api/';
    }

    static getSiteDomain(): string {
        return this.getEnv().protocol + '://' + this.getEnv().siteDomain;
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