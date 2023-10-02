import { of } from "rxjs";
import { UserService } from "./user.service";
import { Config } from "../config";

describe('UserService', () => {
    it('Should fetch data on getUserData call', () => {

        spyOn(Config, 'getDomain').and.returnValue('https://localhost/api/');
        spyOn(Config, 'getHeaders').and.returnValue({ headers: { header: 'header' }});

        const responseData = { 'data': [] };
        const httpSpy = jasmine.createSpyObj('HttpClient', ['get']);
        httpSpy.get.and.returnValue(of(responseData));

        const service = new UserService(httpSpy);

        const actual = service.loadUserData();

        expect(httpSpy.get).toHaveBeenCalledOnceWith(
            'https://localhost/api/user/',
            {
                headers: { header: 'header' }
            }
        );

        actual.subscribe(res => {
            expect(res).toBe(responseData);
        })
    });
});
