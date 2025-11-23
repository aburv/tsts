import { LocalDataService } from './localStore.service';

describe('LocalDataService', () => {
  const KEY = 'TEST_KEY';

  beforeEach(() => {
    localStorage.clear();
  });

  it('Should return null when no data present', () => {
    const service = new LocalDataService(KEY);
    expect(service.getValues()).toBeNull();
  });

  it('Should set and get values correctly', () => {
    const service = new LocalDataService(KEY);
    const obj = { a: 1, b: 'two' };
    service.setValues(obj);

    const read = service.getValues();
    expect(read).toEqual(obj);
  });

  it('Should return null when stored data is corrupted', () => {
    const service = new LocalDataService(KEY);
    localStorage.setItem(KEY, 'not-base64');

    const read = service.getValues();
    expect(read).toBeNull();
  });

  it('Should clear data', () => {
    const service = new LocalDataService(KEY);
    service.setValues({ x: 1 });
    expect(localStorage.getItem(KEY)).toBeTruthy();
    service.clearData();
    expect(localStorage.getItem(KEY)).toBeNull();
  });

  it('Should decode base64 JSON when getItem returns encoded JSON', () => {
    const encoded = btoa(encodeURIComponent(JSON.stringify('data'))); // produces ImRhdGEi-like
    spyOn(localStorage, 'getItem').and.returnValue(encoded);

    const service = new LocalDataService('key');
    const value = service.getValues();

    expect(localStorage.getItem).toHaveBeenCalledOnceWith('key');
    expect(value).toEqual('data');
  });

  it('should call setItem on setValues', () => {
    const setSpy = spyOn(localStorage, 'setItem');
    const service = new LocalDataService('key');
    service.setValues({ foo: 'bar' });
    expect(setSpy).toHaveBeenCalledOnceWith('key', jasmine.any(String));
  });

  it('Should call removeItem on clearData', () => {
    const removeSpy = spyOn(localStorage, 'removeItem');
    const service = new LocalDataService('key');
    service.clearData();
    expect(removeSpy).toHaveBeenCalledOnceWith('key');
  });

  it('Should handle errors during setValues and log them', () => {
    spyOn(localStorage, 'setItem').and.callFake(() => { throw new Error('fail'); });
    const errSpy = spyOn(console, 'error');

    const service = new LocalDataService('key');
    service.setValues({ broken: true });

    expect(errSpy).toHaveBeenCalled();
  });
});