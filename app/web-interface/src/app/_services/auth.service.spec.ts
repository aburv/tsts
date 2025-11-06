import { of } from "rxjs";
import { AuthService } from "./auth.service";
import { Config } from "../config";
import { HttpClient } from "@angular/common/http";
import { TestBed } from "@angular/core/testing";

describe('AuthService', () => {
    let service: AuthService;
    let httpSpy: jasmine.SpyObj<HttpClient>;

    beforeEach(() => {
        httpSpy = jasmine.createSpyObj('HttpClient', ['post', 'get']);

        TestBed.configureTestingModule({
            providers: [
                AuthService,
                { provide: HttpClient, useValue: httpSpy },
            ],
        });

        service = TestBed.inject(AuthService);
    });

    it('Should make a post call on signIn call', () => {
        spyOn(Config, 'getDomain').and.returnValue('https://localhost/api/');
        spyOn(Config, 'getHeaders').and.returnValue({ headers: { header: 'header' } });

        const responseData = { 'data': [] };

        httpSpy.post.and.returnValue(of(responseData));

        const actual = service.signIn({});

        expect(httpSpy.post).toHaveBeenCalledOnceWith(
            'https://localhost/api/auth/login',
            { data: {} },
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

        httpSpy.get.and.returnValue(of(responseData));

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
