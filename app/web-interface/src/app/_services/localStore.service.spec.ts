import { LocalDataService } from "./localStore.service";

describe('Local Data Services', () => {
    it('Should call getItem and return data on getValues call', () => {
        const getSpy = spyOn(localStorage, 'getItem');
        getSpy.and.returnValue('ImRhdGEi');

        const services = new LocalDataService("key");

        const value = services.getValues();

        expect(getSpy).toHaveBeenCalledOnceWith('key');
        expect(value).toBe('data');
    });

    it('Should return null if key is not in storage on getValues call', () => {
        const getSpy = spyOn(localStorage, 'getItem');
        getSpy.and.returnValue(null);

        const services = new LocalDataService('key');

        const value = services.getValues();

        expect(getSpy).toHaveBeenCalledOnceWith('key');
        expect(value).toBe(null);
    });

    it('Should call setItem get on setValues call', () => {
        const setSpy = spyOn(localStorage, 'setItem');

        const services = new LocalDataService('key');

        services.setValues('data');

        expect(setSpy).toHaveBeenCalledOnceWith('key', 'JTIyZGF0YSUyMg==');
    });

    it('Should call removeItem get on clearData call', () => {
        const removeSpy = spyOn(localStorage, 'removeItem');

        const services = new LocalDataService('key');

        services.clearData();

        expect(removeSpy).toHaveBeenCalledOnceWith('key');
    });
});