import { Config } from './config';
import { LocalDataService } from './_services/localStore.service';
import { environment } from '../environments/environment';

describe('Config', () => {
    afterEach(() => {
        try { (LocalDataService.prototype.getValues as any).and?.callThrough?.(); } catch { return }
    });

    it('Should return domain url', () => {
        expect(Config.getNameSpace()).toBe('/api/');
    });

    it('Should return site domain', () => {
        expect(Config.getSiteDomain()).toBe('https://about.takbuff.com');
    });

    it('Should return headers with no access token', () => {
        const expected = { headers: {'content-type': 'application/json', 'x-access-key': '' } };

        const actual = Config.getHeaders();

        expect(actual).toEqual(expected);
    });

    it('getHeaders returns x-access-key with tokens when data present', () => {
        spyOn(LocalDataService.prototype, 'getValues').and.returnValue({ idToken: 'ID', accessToken: 'ACC' });

        const headers = Config.getHeaders();

        expect(headers.headers['x-access-key']).toBe('ID' + environment.separator + 'ACC');
    });

    it('Should return env', () => {
        expect(Config.getEnv()).toEqual({
            production: false,
            authKey: 'aukk',
            separator: '***',
            googleServiceAccount: 'googleServiceAccount'
        });
    });

    it('Should return GCID', () => {
        spyOn(Config, 'getEnv').and.returnValue({ googleServiceAccount: 'googleServiceAccount' } as any);

        expect(Config.getGCID()).toEqual('googleServiceAccount');
    });
});
