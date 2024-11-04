import { Config } from "./config";

describe('Config', () => {

    it('Should return domain url', () => {
        spyOn(Config, 'getEnv').and.returnValue({ protocol: 'https', domain: "localhost" })

        expect(Config.getDomain()).toBe('https://localhost/api/');
    });


    it('Should return site domain', () => {
        spyOn(Config, 'getEnv').and.returnValue({ protocol: 'https', siteDomain: "localhost" })

        expect(Config.getSiteDomain()).toBe('https://localhost');
    });

    it('Should return headers', () => {
        spyOn(Config, 'getEnv').and.returnValue({ key: 'key' })

        expect(Config.getHeaders()).toEqual({ headers: { 'x-api-key': 'key', 'content-type': 'application/json' } });
    });

    it('Should return env', () => {
        expect(Config.getEnv()).toEqual({
            production: false,
            protocol: 'http',
            domain: 'localhost',
            siteDomain: 'localhost',
            key: 'key',
        });
    });
});
