import { of } from "rxjs";
import { DeviceService } from "./device.service";

describe('DeviceService', () => {
    it('Should make a post call on sendDeviceDetails call', () => {
        const responseData = { 'data': "id_from_db" };
        const dataSpy = jasmine.createSpyObj('DataService', ['post']);
        dataSpy.post.and.returnValue(of(responseData));

        const data = {
            deviceId: "deviceId",
            os: "",
            other: "",
            version: "",
            deviceType: "",
            platform: "",
        }

        const service = new DeviceService(dataSpy);

        const getSpy = spyOn(service, 'getValues').and.returnValue(null);       
        const setSpy = spyOn(service,  'setValues');       

        spyOn(service, 'getDeviceInfo').and.returnValue(data)

        service.sendDeviceDetails();

        expect(getSpy).toHaveBeenCalledOnceWith()
        expect(getSpy).toHaveBeenCalledOnceWith()
        expect(service.getDeviceInfo).toHaveBeenCalledOnceWith()
        expect(dataSpy.post).toHaveBeenCalledOnceWith('device/register', {
            deviceId: "deviceId",
            os: "",
            version: "",
            other: "",
            deviceType: "",
            platform: "",
        });

        setSpy.calls.reset();
    });

    it('Should not make a post call when data is present in store on sendDeviceDetails call', () => {
        const responseData = { 'data': "id_from_db" };
        const dataSpy = jasmine.createSpyObj('DataService', ['post']);
        dataSpy.post.and.returnValue(of(responseData));

        const data = {
            deviceId: "deviceId",
            os: "",
            other: "",
            version: "",
            deviceType: "",
            platform: "",
        }

        const service = new DeviceService(dataSpy);

        const getSpy = spyOn(service, 'getValues').and.returnValue({});       
        const setSpy = spyOn(service,  'setValues');       

        spyOn(service, 'getDeviceInfo').and.returnValue(data)

        service.sendDeviceDetails();

        expect(getSpy).toHaveBeenCalledOnceWith();
        expect(setSpy).not.toHaveBeenCalled();
        expect(service.getDeviceInfo).not.toHaveBeenCalled();
        expect(dataSpy.post).not.toHaveBeenCalled();
    });

    it('Should return unknown device data payload on getDeviceInfo call', () => {
        const dataSpy = jasmine.createSpyObj('DataService', ['post']);
        const agent = 'Mozilla/5.0'
        spyOnProperty(window.navigator, 'userAgent').and.returnValue(agent);        
        
        const data = { 
            deviceId: 'device_id', 
            os: 'unknown', 
            version: 'unknown', 
            other: agent, 
            deviceType: 'D', 
            platform: 'B' 
        };

        const service = new DeviceService(dataSpy);

        const actual = service.getDeviceInfo();

        expect(actual).toEqual(data);

    });

    it('Should return windows device data payload on getDeviceInfo call', () => {
        const dataSpy = jasmine.createSpyObj('DataService', ['post']);
        const agent = 'Mozilla/5.0 (Windows NT 10.0; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        spyOnProperty(window.navigator, 'userAgent').and.returnValue(agent);        
        
        const data = { 
            deviceId: 'device_id', 
            os: 'Windows', 
            version: '10.0', 
            other: agent, 
            deviceType: 'D', 
            platform: 'B' 
        };

        const service = new DeviceService(dataSpy);

        const actual = service.getDeviceInfo();

        expect(actual).toEqual(data);

    });

    it('Should return mac device data payload on getDeviceInfo call', () => {
        const dataSpy = jasmine.createSpyObj('DataService', ['post']);
        const agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        spyOnProperty(window.navigator, 'userAgent').and.returnValue(agent);        
        
        const data = { 
            deviceId: 'device_id', 
            os: 'MacOS', 
            version: 'unknown', 
            other: agent, 
            deviceType: 'D', 
            platform: 'B' 
        };

        const service = new DeviceService(dataSpy);

        const actual = service.getDeviceInfo();

        expect(actual).toEqual(data);

    });

    it('Should return android tab device data payload on getDeviceInfo call', () => {
        const dataSpy = jasmine.createSpyObj('DataService', ['post']);
        const agent = 'Mozilla/5.0 (Android; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        spyOnProperty(window.navigator, 'userAgent').and.returnValue(agent);        
        
        const data = { 
            deviceId: 'device_id', 
            os: 'Android', 
            version: 'unknown', 
            other: agent, 
            deviceType: 'T', 
            platform: 'B' 
        };

        const service = new DeviceService(dataSpy);

        const actual = service.getDeviceInfo();

        expect(actual).toEqual(data);

    });

    it('Should return android phone device data payload on getDeviceInfo call', () => {
        const dataSpy = jasmine.createSpyObj('DataService', ['post']);
        const agent = 'Mozilla/5.0 (Mobile; Android; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        spyOnProperty(window.navigator, 'userAgent').and.returnValue(agent);        
        
        const data = { 
            deviceId: 'device_id', 
            os: 'Android', 
            version: 'unknown', 
            other: agent, 
            deviceType: 'P', 
            platform: 'B' 
        };

        const service = new DeviceService(dataSpy);

        const actual = service.getDeviceInfo();

        expect(actual).toEqual(data);

    });

    it('Should return ipad device data payload on getDeviceInfo call', () => {
        const dataSpy = jasmine.createSpyObj('DataService', ['post']);
        const agent = 'Mozilla/5.0 (iPad; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'

        spyOnProperty(window.navigator, 'userAgent').and.returnValue(agent);        
        
        const data = { 
            deviceId: 'device_id', 
            os: 'IOS', 
            version: 'unknown', 
            other: agent, 
            deviceType: 'T', 
            platform: 'B' 
        };

        const service = new DeviceService(dataSpy);

        const actual = service.getDeviceInfo();

        expect(actual).toEqual(data);

    });

    it('Should return iphone device data payload on getDeviceInfo call', () => {
        const dataSpy = jasmine.createSpyObj('DataService', ['post']);
        const agent = 'Mozilla/5.0 (iPhone; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        spyOnProperty(window.navigator, 'userAgent').and.returnValue(agent);        
        
        const data = { 
            deviceId: 'device_id', 
            os: 'IOS', 
            version: 'unknown', 
            other: agent, 
            deviceType: 'P', 
            platform: 'B' 
        };

        const service = new DeviceService(dataSpy);

        const actual = service.getDeviceInfo();

        expect(actual).toEqual(data);

    });

    it('Should return device id from localstorage', () => {
        const dataSpy = jasmine.createSpyObj('DataService', ['post']);

        const service = new DeviceService(dataSpy);

        const getValuesSpy = spyOn(service, 'getValues');
        getValuesSpy.and.returnValue({ 
            id: 'id',
        })

        const actual = service.getDeviceId();

        expect(actual).toEqual("id");
    });
});
