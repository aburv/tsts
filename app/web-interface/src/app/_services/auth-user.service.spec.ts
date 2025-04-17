import { GAuthUser } from "../_models/user";
import { AuthUtils } from "../auth-util";
import { AuthUserService } from "./auth-user.service";

describe('AuthUserService', () => {
    it('Should set the logged Google user', () => {
        const decodeSpy = spyOn<any>(AuthUtils, `decodeJwt`);
        decodeSpy.and.returnValue({
            'sub': 'sub',
            'name': 'name',
            'email': 'email',
            'picture': 'picture',
            'firstName': 'given Name',
            'lastName': 'family name'
        });

        const authService = new AuthUserService();

        authService.handleGoogleResponse({ credential: "token" })

        authService.getLoggedUser().subscribe((user: GAuthUser) => {
            expect(user).toEqual({
                'sub': 'sub',
                'name': 'name',
                'email': 'email',
                'picture': 'picture',
                'firstName': 'given Name',
                'lastName': 'family name'
            });
        });

        expect(decodeSpy).toHaveBeenCalledOnceWith('token');
    });
});
