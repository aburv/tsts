import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Config } from '../config';
import { Observable } from 'rxjs';

function getUserUrl(): string {
  return Config.getDomain() + 'user/';
}

@Injectable({
  providedIn: 'root',
})
export class UserService {
  constructor(private http: HttpClient) { }

  loadUserData(): Observable<any> {
    const url = getUserUrl() + 'app';
    return this.http.get(url, Config.getHeaders());
  }
}
