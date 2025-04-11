import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Config } from '../config';
import { Observable, catchError, of } from 'rxjs';
import { PingService } from './ping.service';

@Injectable({
  providedIn: 'root',
})
export class DataService {
  constructor(
    private http: HttpClient,
    private pingService: PingService
  ) { }

  get(url: string): Observable<any> {
    return this.http.get(Config.getDomain() + url, Config.getHeaders()).pipe(
      catchError((error: HttpErrorResponse) => {
        if (!(error.error instanceof ErrorEvent)) {
          if (error.status === 404 || error.status === 0) {
            this.pingService.ping();
          }
        }
        return of('')
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
