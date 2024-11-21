import { of } from "rxjs";
import { UserService } from "./user.service";

describe('UserService', () => {
    it('Should make a get call on getUserData call', () => {
        const responseData = { 'data': [] };
        const dataSpy = jasmine.createSpyObj('DataService', ['get']);
        dataSpy.get.and.returnValue(of(responseData));

        const service = new UserService(dataSpy);

        const actual = service.getUserData();

        expect(dataSpy.get).toHaveBeenCalledOnceWith('user/app');

        actual.subscribe(res => {
            expect(res).toBe(responseData);
        });
    });
});
