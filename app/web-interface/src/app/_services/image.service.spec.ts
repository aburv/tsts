import { of } from "rxjs";
import { ImageService } from "./image.service";
import { Config } from "../config";
import { signal } from "@angular/core";

describe('ImageService', () => {
    it('Should make a post call on new call', () => {
        const responseData = { 'data': [] };

        spyOn(Config, 'getDomain').and.returnValue('https://host/api/');
        spyOn(Config, 'getHeaders').and.returnValue({ headers: { 'content-type': 'header', header: 'header' } });
        const httpSpy = jasmine.createSpyObj('HttpClient', ['post']);
        const pingSpy = jasmine.createSpyObj('PingService', ['getIsServerDown']);
        pingSpy.getIsServerDown.and.returnValue(signal(false));
        httpSpy.post.and.returnValue(of(responseData));


        const file = new File([], "");

        const service = new ImageService(httpSpy, pingSpy);

        const actual = service.new(file);

        expect(httpSpy.post.calls.mostRecent().args[0]).toEqual('https://host/api/image/add');

        const reqBody = httpSpy.post.calls.mostRecent().args[1] as FormData;
        expect(reqBody instanceof FormData).toBeTrue();
        expect(reqBody.get('file')).toEqual(file);

        const headers = httpSpy.post.calls.mostRecent().args[2];
        expect(headers).toEqual({ headers: { header: 'header' } });

        actual.subscribe(res => {
            expect(res).toBe(responseData);
        })
    });

    it('Should not make a post call when server is down on new call', () => {
        const responseData = {}
        spyOn(Config, 'getDomain').and.returnValue('https://host/api/');
        spyOn(Config, 'getHeaders').and.returnValue({ headers: { 'content-type': 'header', header: 'header' } });
        const httpSpy = jasmine.createSpyObj('HttpClient', ['post']);
        const pingSpy = jasmine.createSpyObj('PingService', ['getIsServerDown']);
        pingSpy.getIsServerDown.and.returnValue(signal(true));
        httpSpy.post.and.returnValue(of(responseData));

        const file = new File([], "");

        const service = new ImageService(httpSpy, pingSpy);

        const actual = service.new(file);

        expect(httpSpy.post).not.toHaveBeenCalled()

        actual.subscribe(res => {
            expect(res).toBe(null);
        })
    });

    it('Should make a get call on get call', () => {
        const responseData = { 'data': [] };
        const httpSpy = jasmine.createSpyObj('HttpClient', ['get']);
        const pingSpy = jasmine.createSpyObj('PingService', ['getIsServerDown']);
        spyOn(Config, 'getDomain').and.returnValue('https://host/api/');
        spyOn(Config, 'getHeaders').and.returnValue({ headers: { header: 'header' } });

        httpSpy.get.and.returnValue(of(responseData));

        const service = new ImageService(httpSpy, pingSpy);

        const actual = service.get("id", "320");

        expect(httpSpy.get).toHaveBeenCalledOnceWith('https://host/api/image/id/320', { responseType: 'blob', headers: { header: 'header' } });

        actual.subscribe(res => {
            expect(res).toBe(responseData);
        })
    });
});
