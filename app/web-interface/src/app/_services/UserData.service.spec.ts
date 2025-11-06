import { of } from "rxjs";
import { UserDataService } from "./UserData.service";
import { AuthUtils } from "../auth-util";
import { TestBed } from "@angular/core/testing";
import { AuthService } from "./auth.service";

describe('User Data Services', () => {
    let service: UserDataService;
    let authSpy: jasmine.SpyObj<AuthService>;

    beforeEach(() => {
        authSpy = jasmine.createSpyObj('AuthService', ['refreshToken', 'signIn']);

        TestBed.configureTestingModule({
            providers: [
                UserDataService,
                { provide: AuthService, useValue: authSpy },
            ],
        });

        service = TestBed.inject(UserDataService);
    });


    it('Should return true, fetch and set updated user idToken into local storage on autoSignIn call', () => {
        const refreshUserTokenSpy = spyOn(service, 'refreshUserToken');
        refreshUserTokenSpy.and.returnValue(of(true))
        const getValueSpy = spyOn(service, 'getValues');
        getValueSpy.and.returnValue({ token: "" });
        const isExpiredSpy = spyOn(service, 'isTokenExpired');
        isExpiredSpy.and.returnValue(true);

        const actual = service.autoSignIn();

        expect(service.isTokenExpired).toHaveBeenCalledOnceWith();
        expect(service.refreshUserToken).toHaveBeenCalledOnceWith();

        actual.subscribe(res => {
            expect(res).toBe(true);
        });

        refreshUserTokenSpy.calls.reset();
        getValueSpy.calls.reset();
        isExpiredSpy.calls.reset();
    });

    it('Should return true on idToken not expired on autoSignIn call', () => {
        const getValueSpy = spyOn(service, 'getValues');
        getValueSpy.and.returnValue({ token: "" })

        const isExpiredSpy = spyOn(service, 'isTokenExpired');
        isExpiredSpy.and.returnValue(false)

        const actual = service.autoSignIn();

        expect(service.isTokenExpired).toHaveBeenCalledOnceWith();

        actual.subscribe(res => {
            expect(res).toBe(true);
        })
    });

    it('Should return false on no user on autoSignIn call', () => {
        const getValueSpy = spyOn(service, 'getValues');
        getValueSpy.and.returnValue(null)

        const actual = service.autoSignIn();

        actual.subscribe(res => {
            expect(res).toBe(false);
        })
    });

    it('Should return true, fetch and set updated user idToken into local storage on refreshUserToken call', () => {
        authSpy.refreshToken.and.returnValue(of({ data: { idToken: "idToken", accessToken: "accessToken" } }));

        const setTokenSpy = spyOn(service, 'setUserTokens');
        setTokenSpy.and.returnValue(true);

        const actual = service.refreshUserToken();

        actual.subscribe(res => {
            expect(res).toBe(true);
        });

        expect(authSpy.refreshToken).toHaveBeenCalledOnceWith();
        expect(service.setUserTokens).toHaveBeenCalledOnceWith({ idToken: "idToken", accessToken: "accessToken" });

        setTokenSpy.calls.reset();
        authSpy.refreshToken.calls.reset();
    });

    it('Should call get on local storage on getValues call', () => {
        const getValueSpy = spyOn(service, 'getValues');
        getValueSpy.and.returnValue('value');

        const values = service.getValues();

        expect(service.getValues).toHaveBeenCalledOnceWith();
        getValueSpy.calls.reset();

        expect(values).toBe('value');
    });

    it('Should call clear on local storage on clear call', () => {
        const clearValueSpy = spyOn(service, 'clearData');

        service.clear();

        expect(service.clearData).toHaveBeenCalledOnceWith();
        clearValueSpy.calls.reset();
    });

    it('Should return unvalues if storage have no token on getUser call', () => {
        const getValueSpy = spyOn(service, 'getValues');
        getValueSpy.and.returnValue(null);

        const data = service.getUser();

        expect(service.getValues).toHaveBeenCalledOnceWith();
        getValueSpy.calls.reset();

        expect(data).toEqual({ dp: "", name: "", email: "" });
    });

    it('Should return values if storage has user on getUser call', () => {
        const getValueSpy = spyOn(service, 'getValues');
        getValueSpy.and.returnValue({ idToken: "token" });
        const decodeJwtSpy = spyOn(AuthUtils, 'decodeJwt');
        decodeJwtSpy.and.returnValue({ user: { dp: "aa", name: "name", user_id: { val: "email" } } });

        const data = service.getUser();

        expect(service.getValues).toHaveBeenCalledOnceWith();
        expect(decodeJwtSpy).toHaveBeenCalledOnceWith("token");
        getValueSpy.calls.reset();

        expect(data).toEqual({ dp: "aa", name: "name", email: "email" });

        decodeJwtSpy.calls.reset();
    });

    it('Should return true and set user token when user on setUserTokens call', () => {
        const getValueSpy = spyOn(service, 'getValues');
        getValueSpy.and.returnValue({ dp: "aa", name: "name", email: "email" });
        const setValueSpy = spyOn(service, 'setValues');

        const actual = service.setUserTokens({ idToken: "idToken", accessToken: "accessToken" });

        expect(service.getValues).toHaveBeenCalledOnceWith();
        expect(service.setValues).toHaveBeenCalledOnceWith(
            {
                dp: "aa", name: "name", email: "email",
                idToken: 'idToken', accessToken: 'accessToken'
            }
        );

        expect(actual).toBeTrue();

        setValueSpy.calls.reset();
        getValueSpy.calls.reset();
    });

    it('Should return false set user token when no token on setUserTokens call', () => {
        const getValueSpy = spyOn(service, 'getValues');
        getValueSpy.and.returnValue({ dp: "aa", name: "name", email: "email" });
        const setValueSpy = spyOn(service, 'setValues');

        const actual = service.setUserTokens({ idToken: "idToken", accessToken: "" });

        expect(service.getValues).not.toHaveBeenCalledOnceWith();
        expect(service.setValues).not.toHaveBeenCalled();

        expect(actual).toBeFalse();

        setValueSpy.calls.reset();
        getValueSpy.calls.reset();
    });

    it('Should set user token on signIn call', () => {
        authSpy.signIn.and.returnValue(of({ data: { idToken: "token", accessToken: "accessToken" } }));

        const setTokenSpy = spyOn(service, 'setUserTokens');
        setTokenSpy.and.returnValue(true);

        const actual = service.signIn({ user: {}, login: {} });

        actual.subscribe((res) => {
            expect(res).toBe(true);
        })

        expect(service.setUserTokens).toHaveBeenCalledOnceWith({ idToken: "token", accessToken: "accessToken" });

        setTokenSpy.calls.reset();
    });

    it('Should return user access token when user on getAccessToken call', () => {
        const getValueSpy = spyOn(service, 'getValues');
        getValueSpy.and.returnValue({ 'accessToken': "token" });

        const actual = service.getAccessToken();

        expect(service.getValues).toHaveBeenCalledOnceWith();

        expect(actual).toBe("token");
    });

    it('Should return empty string when no user on getAccessToken call', () => {
        const getValueSpy = spyOn(service, 'getValues');
        getValueSpy.and.returnValue(null);

        const actual = service.getAccessToken();

        expect(service.getValues).toHaveBeenCalledOnceWith();

        expect(actual).toBe("");
    });

    it('Should return true on isTokenExpired call', () => {
        const decodeJwtSpy = spyOn(AuthUtils, "decodeJwt");
        decodeJwtSpy.and.returnValue({ exp: 10000000000 });
        const getAccessTokenSpy = spyOn(service, "getAccessToken");
        getAccessTokenSpy.and.returnValue("token");

        const actual = service.isTokenExpired();

        expect(actual).toBe(true);
        expect(decodeJwtSpy).toHaveBeenCalledOnceWith("token");
        expect(getAccessTokenSpy).toHaveBeenCalledOnceWith();

        getAccessTokenSpy.calls.reset();
        decodeJwtSpy.calls.reset();
    });
});
