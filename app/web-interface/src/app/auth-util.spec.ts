import { AuthUtils } from "./auth-util";

describe('Auth Utils', () => {
    it('Should decodeJWT ', () => {
        const idToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c';

        const mockBase64Url = 'eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ';
        const mockBase64 = 'eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ';

        const responseObj = { sub: "1234567890", name: "John Doe", iat: "1516239022" }

        // spyOn(idToken, 'split').and.returnValue(["", mockBase64Url]);        
        // spyOn(mockBase64Url, 'replace').and.returnValue(mockBase64);
        spyOn(window, 'atob').and.returnValue(mockBase64Url);
        spyOn(window, 'decodeURIComponent').and.returnValue(responseObj.toString());
        spyOn(JSON, 'parse').and.returnValue(responseObj);

        const result = AuthUtils.decodeJwt(idToken);

        expect(atob).toHaveBeenCalledWith(mockBase64);
        expect(JSON.parse).toHaveBeenCalledWith(responseObj.toString());
        
        expect(result).toEqual(responseObj);
    });
});
