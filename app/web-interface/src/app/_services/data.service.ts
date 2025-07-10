import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Config } from '../config';
import { Observable, catchError, of, switchMap } from 'rxjs';
import { PingService } from './ping.service';
import { UserDataService } from './UserData.service';

@Injectable({
  providedIn: 'root',
})
export class DataService {
  constructor(
    private http: HttpClient,
    private pingService: PingService,
    private userData: UserDataService
  ) { }

  get(path: string): Observable<any> {
    const url = Config.getDomain() + path;
    return this.http.get(url, Config.getHeaders()).pipe(
      catchError((error: HttpErrorResponse) => {
        if (!(error.error instanceof ErrorEvent)) {
          if (error.status === 401) {
            return this.userData.refreshUserToken().pipe(
              switchMap((isDone: boolean) => {
                if (isDone) {
                  return this.http.get(url, Config.getHeaders());
                }
                return of('');
              })
            );
          }
          if (error.status === 404 || error.status === 0) {
            this.pingService.ping();
            return of('');
          }
        }
        return of('');
      })
    );
  }

  post(url: string, data: any): Observable<any> {
    if (!PingService.isServerDown()) {
      return this.http.post(Config.getDomain() + url, { data }, Config.getHeaders());
    }
    return of(null)
  }
}
