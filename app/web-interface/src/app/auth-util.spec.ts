import { AuthUtils } from "./auth-util";

describe('Auth Utils', () => {
    it('Should decodeJWT ', () => {
        const idToken: string = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c';

        const mockBase64Url = 'eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ';
        const mockBase64 = 'eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ';

        spyOn(idToken, 'split').and.returnValue(["", mockBase64Url]);        
        spyOn(mockBase64Url, 'replace').and.returnValue(mockBase64);
        spyOn(window, 'atob').and.returnValue('eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ');
        spyOn(window, 'decodeURIComponent').and.returnValue('{"sub":"1234567890","name":"John Doe", "iat":"1516239022"}');
        spyOn(JSON, 'parse').and.returnValue({ sub: "1234567890", name: "John Doe", iat: "1516239022" });

        const result = AuthUtils.decodeJwt(idToken);

        expect(atob).toHaveBeenCalledWith(mockBase64);
        expect(JSON.parse).toHaveBeenCalledWith('{"sub":"1234567890","name":"John Doe", "iat":"1516239022"}');
        
        expect(result).toEqual({ sub: "1234567890", name: "John Doe", "iat": "1516239022" });
    });
});
