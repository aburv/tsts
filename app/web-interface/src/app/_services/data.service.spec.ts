import { of, throwError } from "rxjs";
import { Config } from "../config";
import { DataService } from "./data.service";
import { PingService } from "./ping.service";
import { HttpClient } from "@angular/common/http";
import { UserDataService } from "./UserData.service";
import { TestBed } from "@angular/core/testing";

describe('DataService', () => {
    let service: DataService;
    let httpSpy: jasmine.SpyObj<HttpClient>;
    let pingSpy: jasmine.SpyObj<PingService>;
    let userDataSpy: jasmine.SpyObj<UserDataService>;

    beforeEach(() => {
        httpSpy = jasmine.createSpyObj('HttpClient', ['post', 'get']);
        pingSpy = jasmine.createSpyObj('PingService', ['ping']);
        userDataSpy = jasmine.createSpyObj('UserDataService', ['refreshUserToken']);

        TestBed.configureTestingModule({
            providers: [
                DataService,
                { provide: HttpClient, useValue: httpSpy },
                { provide: PingService, useValue: pingSpy },
                { provide: UserDataService, useValue: userDataSpy },
            ],
        });

        service = TestBed.inject(DataService);
    });

    it('Should return the response data on 200 on get call', () => {
        spyOn(Config, 'getDomain').and.returnValue('https://localhost/api/');
        spyOn(Config, 'getHeaders').and.returnValue({ headers: { header: 'header' } });

        const responseData = { 'data': [] };
        httpSpy.get.and.returnValue(of(responseData));

        const actual = service.get('url/path');

        expect(httpSpy.get).toHaveBeenCalledOnceWith(
            'https://localhost/api/url/path',
            {
                headers: { header: 'header' }
            }
        );

        actual.subscribe(res => {
            expect(res).toBe(responseData);
        })
    });

    it('Should call ping the server on 404 on get call', () => {
        spyOn(Config, 'getDomain').and.returnValue('https://localhost/api/');
        spyOn(Config, 'getHeaders').and.returnValue({ headers: { header: 'header' } });

        httpSpy.get.and.returnValue(throwError(() => { return { status: 404, statusText: "Not Found" } }));

        const actual = service.get('url/path');

        expect(httpSpy.get).toHaveBeenCalledOnceWith(
            'https://localhost/api/url/path',
            {
                headers: { header: 'header' }
            }
        );

        actual.subscribe(res => {
            expect(res).toBe('');
        })

        expect(pingSpy.ping).toHaveBeenCalledOnceWith();
    });

    it('Should call ping the server on 0 on get call', () => {
        spyOn(Config, 'getDomain').and.returnValue('https://localhost/api/');
        spyOn(Config, 'getHeaders').and.returnValue({ headers: { header: 'header' } });

        httpSpy.get.and.returnValue(throwError(() => { return { status: 0, statusText: "Not Found" } }));

        const actual = service.get('url/path');

        expect(httpSpy.get).toHaveBeenCalledOnceWith(
            'https://localhost/api/url/path',
            {
                headers: { header: 'header' }
            }
        );

        actual.subscribe(res => {
            expect(res).toBe('');
        })

        expect(pingSpy.ping).toHaveBeenCalledOnceWith();
    });

    it('Should call refresh token and retry on success get when 401 status on get call', () => {
        spyOn(Config, 'getDomain').and.returnValue('https://localhost/api/');
        spyOn(Config, 'getHeaders').and.returnValue({ headers: { header: 'header' } });

        const responseData = { 'data': [] };
        httpSpy.get.and.returnValues(
            throwError(() => { return { status: 401, statusText: "UnAuthenticated" } }),
            of(responseData)
        );

        userDataSpy.refreshUserToken.and.returnValue(of(true))

        const actual = service.get('url/path');

        expect(httpSpy.get).toHaveBeenCalledOnceWith(
            'https://localhost/api/url/path',
            {
                headers: { header: 'header' }
            }
        );

        actual.subscribe(res => {
            expect(res).toBe(responseData);
        })

        expect(userDataSpy.refreshUserToken).toHaveBeenCalledOnceWith();
    });

    it('Should call refresh token and no retry on failure get when 401 status on get call', () => {
        spyOn(Config, 'getDomain').and.returnValue('https://localhost/api/');
        spyOn(Config, 'getHeaders').and.returnValue({ headers: { header: 'header' } });

        httpSpy.get.and.returnValue(throwError(() => { return { status: 401, statusText: "UnAuthenticated" } }));

        userDataSpy.refreshUserToken.and.returnValue(of(false))

        const actual = service.get('url/path');

        expect(httpSpy.get).toHaveBeenCalledOnceWith(
            'https://localhost/api/url/path',
            {
                headers: { header: 'header' }
            }
        );

        actual.subscribe(res => {
            expect(res).toBe('');
        })

        expect(userDataSpy.refreshUserToken).toHaveBeenCalledOnceWith();
    });

    it('Should call ping the server on other statuses on get call', () => {
        spyOn(Config, 'getDomain').and.returnValue('https://localhost/api/');
        spyOn(Config, 'getHeaders').and.returnValue({ headers: { header: 'header' } });

        httpSpy.get.and.returnValue(throwError(() => { return { status: 305, statusText: "Not Found" } }));

        const actual = service.get('url/path');

        expect(httpSpy.get).toHaveBeenCalledOnceWith(
            'https://localhost/api/url/path',
            {
                headers: { header: 'header' }
            }
        );

        actual.subscribe(res => {
            expect(res).toBe('');
        })

        expect(pingSpy.ping).not.toHaveBeenCalledOnceWith();
        expect(userDataSpy.refreshUserToken).not.toHaveBeenCalledOnceWith();
    });

    it('Should send data and return response data if not isServerDown on post call', () => {
        spyOn(Config, 'getDomain').and.returnValue('https://localhost/api/');
        spyOn(Config, 'getHeaders').and.returnValue({ headers: { header: 'header' } });

        const responseData = { 'data': [] };
        httpSpy.post.and.returnValue(of(responseData));

        PingService.isServerDown.set(false);

        userDataSpy.refreshUserToken.and.returnValue(of(true))

        const actual = service.post('url/path', {});

        expect(httpSpy.post).toHaveBeenCalledOnceWith(
            'https://localhost/api/url/path',
            { data: {} },
            {
                headers: { header: 'header' }
            }
        );

        actual.subscribe(res => {
            expect(res).toBe(responseData);
        })
    });

    it('Should not send data and return null if isServerDown on post call', () => {
        spyOn(Config, 'getDomain').and.returnValue('https://localhost/api/');
        spyOn(Config, 'getHeaders').and.returnValue({ headers: { header: 'header' } });

        const responseData = { 'data': [] };
        httpSpy.post.and.returnValue(of(responseData));

        PingService.isServerDown.set(true);

        userDataSpy.refreshUserToken.and.returnValue(of(true))

        const actual = service.post('url/path', {});

        expect(httpSpy.post).not.toHaveBeenCalled();

        actual.subscribe(res => {
            expect(res).toBe(null);
        })
    });
});
