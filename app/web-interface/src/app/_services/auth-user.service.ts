import { EventEmitter, Injectable } from "@angular/core";
import { AuthUtils } from "../auth-util";
import { GAuthUser } from "../_models/user";
import { Observable } from "rxjs";


@Injectable({
  providedIn: 'root',
})
export class AuthUserService {
  private static user = new EventEmitter<GAuthUser>();

  getLoggedUser(): Observable<GAuthUser> {
    return AuthUserService.user;
  }

  handleGoogleResponse(response: any) {
    const user: GAuthUser = AuthUtils.decodeJwt(response.credential)
    AuthUserService.user.emit(user);
  }
}
