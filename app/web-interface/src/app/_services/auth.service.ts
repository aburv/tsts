import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Config } from '../config';

function getAuthUrl(): string {
  return Config.getDomain() + 'auth/';
}


@Injectable({
  providedIn: 'root',
})
export class AuthService {
  constructor(private http: HttpClient) { }

  signIn(userLoginData: any): Observable<any> {
    return this.http.post(getAuthUrl() + 'login', { data: userLoginData }, Config.getHeaders());
  }

  refreshToken(): Observable<any> {
    return this.http.get(getAuthUrl() + "refresh_token", Config.getHeaders());
  }
}
