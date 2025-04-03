import { of, throwError } from "rxjs";
import { Config } from "../config";
import { PingService } from "./ping.service";

describe('PingService', () => {
    it('Should emit false on isServerDown 200 status on ping call', () => {
        spyOn(Config, 'getDomain').and.returnValue('https://localhost/api/');
        spyOn(Config, 'getHeaders').and.returnValue({ headers: { header: 'header' } });

        const responseData = { 'data': [] };
        const httpSpy = jasmine.createSpyObj('HttpClient', ['post']);
        httpSpy.post.and.returnValue(of(responseData));

        const service = new PingService(httpSpy);

        service.ping();

        expect(httpSpy.post).toHaveBeenCalledOnceWith(
            'https://localhost/api/ping/',
            {
                headers: { header: 'header' }
            }
        );

        expect(service.getIsServerDown()()).toEqual(false);
    });

    it('Should emit true on isServerDown on 404 status on ping call', () => {
        spyOn(Config, 'getDomain').and.returnValue('https://localhost/api/');
        spyOn(Config, 'getHeaders').and.returnValue({ headers: { header: 'header' } });

        const httpSpy = jasmine.createSpyObj('HttpClient', ['post']);
        httpSpy.post.and.returnValue(throwError(() => { return { status: 404, statusText: "Not Found" } }));

        const service = new PingService(httpSpy);

        service.ping();

        expect(httpSpy.post).toHaveBeenCalledOnceWith(
            'https://localhost/api/ping/',
            {
                headers: { header: 'header' }
            }
        );

        expect(service.getIsServerDown()()).toEqual(true);
    });

    it('Should emit true on isServerDown on 0 status on ping call', () => {
        spyOn(Config, 'getDomain').and.returnValue('https://localhost/api/');
        spyOn(Config, 'getHeaders').and.returnValue({ headers: { header: 'header' } });

        const httpSpy = jasmine.createSpyObj('HttpClient', ['post']);
        httpSpy.post.and.returnValue(throwError(() => { return { status: 0, statusText: "Not Found" } }));

        const service = new PingService(httpSpy);

        service.ping();

        expect(httpSpy.post).toHaveBeenCalledOnceWith(
            'https://localhost/api/ping/',
            {
                headers: { header: 'header' }
            }
        );

        expect(service.getIsServerDown()()).toEqual(true);
    });

    it('Should emit false on isServerDown other than 404,0 status errors  on ping call', () => {
        spyOn(Config, 'getDomain').and.returnValue('https://localhost/api/');
        spyOn(Config, 'getHeaders').and.returnValue({ headers: { header: 'header' } });

        const httpSpy = jasmine.createSpyObj('HttpClient', ['post']);
        httpSpy.post.and.returnValue(throwError(() => { return { status: 401, statusText: "Not Found" } }));

        const service = new PingService(httpSpy);

        service.ping();

        expect(httpSpy.post).toHaveBeenCalledOnceWith(
            'https://localhost/api/ping/',
            {
                headers: { header: 'header' }
            }
        );

        expect(service.getIsServerDown()()).toEqual(false);
    });
});
