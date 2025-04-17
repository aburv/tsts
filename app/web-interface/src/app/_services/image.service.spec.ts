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
            expect(res).toEqual(responseData);
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

    it('Should make a getAndCachedImage with url call on get call', () => {
        const expectedResult: ArrayBuffer = new ArrayBuffer(8);
        const getDomainSpy = spyOn(Config, 'getDomain').and.returnValue('https://host/api/');
        const httpSpy = jasmine.createSpyObj('HttpClient', ['get']);

        const service = new ImageService(httpSpy);

       const getAndCachedImageSpy = spyOn(service, 'getAndCachedImage');
       getAndCachedImageSpy.and.returnValue(of(expectedResult));

        const actual = service.get('id', '320');

        expect(getDomainSpy).toHaveBeenCalledOnceWith();

        expect(getAndCachedImageSpy).toHaveBeenCalledOnceWith('https://host/api/image/id/320');

        actual.subscribe(res => {
            expect(res).toEqual(expectedResult);
        })

        getDomainSpy.calls.reset();
    });

    it('Should make a get call and set cache when no data in cache on getAndCachedImage call', () => {
        const expectedResult: ArrayBuffer = new ArrayBuffer(8);
        const getHeaderSpy = spyOn(Config, 'getHeaders').and.returnValue({ headers: { header: 'header' } });
        const httpSpy = jasmine.createSpyObj('HttpClient', ['get']);
        httpSpy.get.and.returnValue(of(expectedResult));

        const service = new ImageService(httpSpy);
        const getFromCacheSpy = spyOn(service, 'getFromCache').and.returnValue(undefined);
        const setCacheSpy = spyOn(service, 'setCache');

        const actual = service.getAndCachedImage('https://host/api/image/id/320');

        expect(getHeaderSpy).toHaveBeenCalledOnceWith();

        expect(httpSpy.get).toHaveBeenCalledOnceWith('https://host/api/image/id/320', { responseType: 'blob', headers: { header: 'header' } });

        actual.subscribe(res => {
            expect(setCacheSpy).toHaveBeenCalledOnceWith('https://host/api/image/id/320', expectedResult);
            expect(res).toEqual(expectedResult);
        });

        getHeaderSpy.calls.reset();
        getFromCacheSpy.calls.reset();
        setCacheSpy.calls.reset();
        httpSpy.get.calls.reset();
    });

    it('Should return cached data and not make a get call when data in cache on getAndCachedImage call', () => {
        const expectedResult: ArrayBuffer = new ArrayBuffer(8);
        const getHeaderSpy = spyOn(Config, 'getHeaders').and.returnValue({ headers: { header: 'header' } });
        const httpSpy = jasmine.createSpyObj('HttpClient', ['get']);

        const service = new ImageService(httpSpy);
        const getFromCacheSpy = spyOn(service, 'getFromCache').and.returnValue(expectedResult);

        const actual = service.getAndCachedImage('https://host/api/image/id/320');

        expect(httpSpy.get).not.toHaveBeenCalled();

        actual.subscribe(res => {
            expect(res).toEqual(expectedResult);
        });
        
        getHeaderSpy.calls.reset();
        getFromCacheSpy.calls.reset();
        httpSpy.get.calls.reset();
    });

    it('Should set and get cache on setCache and getFrom cache calls', () => {
        const expectedResult: ArrayBuffer = new ArrayBuffer(8);

        const httpSpy = jasmine.createSpyObj('HttpClient', ['get']);

        const service = new ImageService(httpSpy);

        const initialCache = service.getFromCache('https://host/api/image/id/320');

        expect(initialCache).toEqual(undefined)

        service.setCache('https://host/api/image/id/320', expectedResult);

        const afterCaching = service.getFromCache('https://host/api/image/id/320');

        expect(afterCaching).toEqual(expectedResult)
    });
});
