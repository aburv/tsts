import {Injectable, Signal, signal} from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class LoaderService {
  static status = signal<boolean>(false);

  loadingOn(): void{
    LoaderService.status.set(true);
  }

  loadingOff(): void{
    LoaderService.status.set(false);
  }
}
