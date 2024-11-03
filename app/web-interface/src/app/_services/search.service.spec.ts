import { of } from "rxjs";
import { SearchService } from "./search.service";

describe('SearchService', () => {
    it('Should make a get call on get search call', () => {
        const responseData = { 'data': [] };
        const dataSpy = jasmine.createSpyObj('DataService', ['get']);
        dataSpy.get.and.returnValue(of(responseData));

        const service = new SearchService(dataSpy);

        const actual = service.get("searching_text");

        expect(dataSpy.get).toHaveBeenCalledOnceWith('search/searching_text');

        actual.subscribe(res => {
            expect(res).toBe(responseData);
        })
    });
});
