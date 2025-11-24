import { Injectable, inject } from '@angular/core';
import { map, Observable, of } from 'rxjs';
import { LocalDataService } from './localStore.service';
import { AuthService } from './auth.service';
import { Config } from '../config';
import { AppUser } from '../_models/user';
import { AuthUtils } from '../auth-util';


@Injectable({
  providedIn: 'root',
})
export class UserDataService extends LocalDataService {
  private service = inject(AuthService);

  constructor() {
    super(Config.getEnv().authKey);
  }

  autoSignIn(): Observable<boolean> {
    const data = this.getValues();
    if (data === null) {
      return of(false);
    }
    else {
      if (this.isTokenExpired()) {
        this.refreshUserToken();
      }
      return of(true);
    }
  }

  signIn(data: any): Observable<boolean> {
    return this.service.signIn(data).pipe(
      map((res: any) => {
        return this.setUserTokens(res['data']);
      })
    );
  }

  refreshUserToken(): Observable<boolean> {
    return this.service.refreshToken().pipe(
      map((res: any) => {
        return this.setUserTokens(res['data']);
      })
    );
  }

  setUserTokens(tokens: { idToken: string, accessToken: string }): boolean {
    if (tokens["idToken"] && tokens["accessToken"]) {
      let data = this.getValues();
      data = { ...data, ...tokens }
      this.setValues(data);
      return true;
    }
    return false;
  }

  isTokenExpired(): boolean {
    const exp = AuthUtils.decodeJwt(this.getAccessToken())["exp"]
    return exp < this.today()
  }

  today(): number {
    return Date.now()
  }

  getAccessToken(): any {
    const data = this.getValues();
    return data === null ? "" : data['accessToken']
  }

  getUser(): AppUser {
    const storageData = this.getValues();
    const data = storageData === null ? null : AuthUtils.decodeJwt(storageData['idToken']);
    return (data === null ? {
      name: "", email: "", dp: ""
    } : {
      name: data["user"]['name'], email: data["user"]["user_id"]['val'], dp: data["user"]['dp']
    });
  }

  clear(): void {
    this.clearData();
  }
}
