import { of, throwError } from "rxjs";
import { Config } from "../config";
import { PingService } from "./ping.service";
import { TestBed } from "@angular/core/testing";
import { HttpClient } from "@angular/common/http";

describe('PingService', () => {
    let service: PingService;
    let httpSpy: jasmine.SpyObj<HttpClient>;

    beforeEach(() => {
        httpSpy = jasmine.createSpyObj('HttpClient', ['post']);

        TestBed.configureTestingModule({
            providers: [
                PingService,
                { provide: HttpClient, useValue: httpSpy },
            ],
        });

        service = TestBed.inject(PingService);
    });

    it('Should emit false on isServerDown 200 status on ping call', () => {
        spyOn(Config, 'getDomain').and.returnValue('https://localhost/api/');
        spyOn(Config, 'getHeaders').and.returnValue({ headers: { header: 'header' } });

        const responseData = { 'data': [] };
        httpSpy.post.and.returnValue(of(responseData));

        service.ping();

        expect(httpSpy.post).toHaveBeenCalledOnceWith(
            'https://localhost/api/ping/',
            {
                headers: { header: 'header' }
            }
        );

        expect(PingService.isServerDown()).toEqual(false);
    });

    it('Should emit true on isServerDown on 404 status on ping call', () => {
        spyOn(Config, 'getDomain').and.returnValue('https://localhost/api/');
        spyOn(Config, 'getHeaders').and.returnValue({ headers: { header: 'header' } });

        httpSpy.post.and.returnValue(throwError(() => { return { status: 404, statusText: "Not Found" } }));

        service.ping();

        expect(httpSpy.post).toHaveBeenCalledOnceWith(
            'https://localhost/api/ping/',
            {
                headers: { header: 'header' }
            }
        );

        expect(PingService.isServerDown()).toEqual(true);
    });

    it('Should emit true on isServerDown on 0 status on ping call', () => {
        spyOn(Config, 'getDomain').and.returnValue('https://localhost/api/');
        spyOn(Config, 'getHeaders').and.returnValue({ headers: { header: 'header' } });

        httpSpy.post.and.returnValue(throwError(() => { return { status: 0, statusText: "Not Found" } }));

        service.ping();

        expect(httpSpy.post).toHaveBeenCalledOnceWith(
            'https://localhost/api/ping/',
            {
                headers: { header: 'header' }
            }
        );

        expect(PingService.isServerDown()).toEqual(true);
    });

    it('Should emit false on isServerDown other than 404,0 status errors  on ping call', () => {
        spyOn(Config, 'getDomain').and.returnValue('https://localhost/api/');
        spyOn(Config, 'getHeaders').and.returnValue({ headers: { header: 'header' } });

        httpSpy.post.and.returnValue(throwError(() => { return { status: 401, statusText: "Not Found" } }));

        service.ping();

        expect(httpSpy.post).toHaveBeenCalledOnceWith(
            'https://localhost/api/ping/',
            {
                headers: { header: 'header' }
            }
        );

        expect(PingService.isServerDown()).toEqual(false);
    });
});
