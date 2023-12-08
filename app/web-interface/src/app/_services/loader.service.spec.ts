import { EventEmitter } from "@angular/core";
import { LoaderService } from "./loader.service";

describe('LoaderService', () => {
  it('Should set emit true on loadingOn call', () => {
    const emitSpy = spyOn(EventEmitter.prototype, 'emit');

    const service = new LoaderService();

    service.loadingOn();

    expect(emitSpy).toHaveBeenCalledOnceWith(true);
  });

  it('Should set emit false on loadingOff call', () => {
    const emitSpy = spyOn(EventEmitter.prototype, 'emit');

    const service = new LoaderService();

    service.loadingOff();

    expect(emitSpy).toHaveBeenCalledOnceWith(false);
  });

  it('Should get loading state emitters', () => {
    const service = new LoaderService();

    const loading = service.getIsLoading();

    expect(loading).toBeInstanceOf(EventEmitter);
  });
});
