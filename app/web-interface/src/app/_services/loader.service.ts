import {EventEmitter, Injectable} from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class LoaderService {
  private isLoading = new EventEmitter<boolean>();

  getIsLoading(): Observable<boolean>{
    return this.isLoading;
  }

  loadingOn(): void{
    this.isLoading.emit(true);
  }

  loadingOff(): void{
    this.isLoading.emit(false);
  }

}