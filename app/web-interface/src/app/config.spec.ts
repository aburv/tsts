import { Config } from "./config";

describe('Config', () => {

    it('Should return domain url', () => {
        expect(Config.getDomain()).toBe('/api/');
    });

    it('Should return site domain', () => {
        spyOn(Config, 'getEnv').and.returnValue({ siteDomain: "http://localhost" })

        expect(Config.getSiteDomain()).toBe('http://localhost');
    });

    it('Should return headers with no access token', () => {
        const expected = { headers: { 'x-api-key': 'key', 'content-type': 'application/json', 'x-access-key': '' } }
        
        const actual =  Config.getHeaders()

        expect(actual).toEqual(expected);
    });

    it('Should return env', () => {
        expect(Config.getEnv()).toEqual({
            production: false,
            siteDomain: 'localhost',
            key: 'key',
            authKey: 'aukk',
            separator: '***',
            googleServiceAccount: 'googleServiceAccount'
        });
    });

    it('Should return GCID', () => {
        spyOn(Config, 'getEnv').and.returnValue({ googleServiceAccount: 'googleServiceAccount' })

        expect(Config.getGCID()).toEqual('googleServiceAccount');
    });
});
