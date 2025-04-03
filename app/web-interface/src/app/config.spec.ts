import { Config } from "./config";

describe('Config', () => {

    it('Should return domain url', () => {
        spyOn(Config, 'getEnv').and.returnValue({ domain: "localhost" })

        expect(Config.getDomain()).toBe('http://localhost/api/');
    });


    it('Should return site domain', () => {
        spyOn(Config, 'getEnv').and.returnValue({ siteDomain: "localhost" })

        expect(Config.getSiteDomain()).toBe('http://localhost');
    });

    it('Should return headers', () => {
        spyOn(Config, 'getEnv').and.returnValue({ key: 'key' })

        expect(Config.getHeaders()).toEqual({ headers: { 'x-api-key': 'key', 'content-type': 'application/json' } });
    });

    it('Should return env', () => {
        expect(Config.getEnv()).toEqual({
            production: false,
            domain: 'localhost',
            siteDomain: 'localhost',
            key: 'key',
        });
    });
});
