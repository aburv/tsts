import { LoaderService } from "./loader.service";

describe('LoaderService', () => {
  it('Should set true on loadingOn call', () => {
    const service = new LoaderService();

    service.loadingOn();

    expect(LoaderService.status()).toBe(true);
  });

  it('Should set false on loadingOff call', () => {
    const service = new LoaderService();

    service.loadingOff();

    expect(LoaderService.status()).toBe(false);
  });

});
