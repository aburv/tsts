import { of } from "rxjs";
import { AuthService } from "./auth.service";
import { Config } from "../config";

describe('AuthService', () => {

    it('Should make a post call on signIn call', () => {
        spyOn(Config, 'getDomain').and.returnValue('https://localhost/api/');
        spyOn(Config, 'getHeaders').and.returnValue({ headers: { header: 'header' } });

        const responseData = { 'data': [] };

        const httpSpy = jasmine.createSpyObj('HttpClient', ['post']);
        httpSpy.post.and.returnValue(of(responseData));

        const service = new AuthService(httpSpy);

        const actual = service.signIn({});

        expect(httpSpy.post).toHaveBeenCalledOnceWith(
            'https://localhost/api/auth/login',
            { data : {}},
            {
                headers: { header: 'header' }
            }
        );

        actual.subscribe(res => {
            expect(res).toBe(responseData);
        })
    });

    it('Should make a get call on refreshToken call', () => {
        spyOn(Config, 'getDomain').and.returnValue('https://localhost/api/');
        spyOn(Config, 'getHeaders').and.returnValue({ headers: { header: 'header' } });

        const responseData = { 'data': [] };

        const httpSpy = jasmine.createSpyObj('HttpClient', ['get']);
        httpSpy.get.and.returnValue(of(responseData));

        const service = new AuthService(httpSpy);

        const actual = service.refreshToken();


        expect(httpSpy.get).toHaveBeenCalledOnceWith(
            'https://localhost/api/auth/refresh_token',
            {
                headers: { header: 'header' }
            }
        );

        actual.subscribe(res => {
            expect(res).toBe(responseData);
        })
    });
});
