import { of } from "rxjs";
import { ImageService } from "./image.service";
import { Config } from "../config";
import { PingService } from "./ping.service";

describe('ImageService', () => {
    it('Should make a post call on new call', () => {
        const responseData = { 'data': [] };

        spyOn(Config, 'getDomain').and.returnValue('https://host/api/');
        spyOn(Config, 'getHeaders').and.returnValue({ headers: { 'content-type': 'header', header: 'header' } });
        const httpSpy = jasmine.createSpyObj('HttpClient', ['post']);
        httpSpy.post.and.returnValue(of(responseData));
        PingService.isServerDown.set(false);

        const file = new File([], "");

        const service = new ImageService(httpSpy);

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
        httpSpy.post.and.returnValue(of(responseData));
        PingService.isServerDown.set(true);

        const file = new File([], "");

        const service = new ImageService(httpSpy);

        const actual = service.new(file);

        expect(httpSpy.post).not.toHaveBeenCalled()

        actual.subscribe(res => {
            expect(res).toBe(null);
        })
    });

    it('Should make a get call on get call', () => {
        const responseData = { 'data': [] };
        spyOn(Config, 'getDomain').and.returnValue('https://host/api/');
        spyOn(Config, 'getHeaders').and.returnValue({ headers: { header: 'header' } });
        const httpSpy = jasmine.createSpyObj('HttpClient', ['get']);
        httpSpy.get.and.returnValue(of(responseData));
        PingService.isServerDown.set(false);

        const service = new ImageService(httpSpy);

        const actual = service.get("id", "320");

        expect(httpSpy.get).toHaveBeenCalledOnceWith('https://host/api/image/id/320', { responseType: 'blob', headers: { header: 'header' } });

        actual.subscribe(res => {
            expect(res).toBe(responseData);
        })
    });
});
