import { Config } from "./config";

describe('Config', () => {

    it('Should return domain url', () => {
        spyOn(Config, 'getEnv').and.returnValue({ domain: "localhost" })
        spyOn(Config, 'getApiProtocol').and.returnValue('http')

        expect(Config.getDomain()).toBe('http://localhost/api/');
    });

    it('Should return http api protocol url', () => {
        spyOn(Config, 'getEnv').and.returnValue({ production: false })

        expect(Config.getApiProtocol()).toBe('http');
    });

    it('hould return https api protocol', () => {
        spyOn(Config, 'getEnv').and.returnValue({ production: true })

        expect(Config.getApiProtocol()).toBe('https');
    });


    it('Should return site domain', () => {
        spyOn(Config, 'getEnv').and.returnValue({ siteDomain: "localhost" })
        spyOn(Config, 'getApiProtocol').and.returnValue('http')

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
            domain: 'localhost',
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
