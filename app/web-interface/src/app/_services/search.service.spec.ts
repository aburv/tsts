import { of } from "rxjs";
import { SearchService } from "./search.service";
import { DataService } from "./data.service";
import { TestBed } from "@angular/core/testing";

describe('SearchService', () => {
  let service: SearchService;
  let dataSpy: jasmine.SpyObj<DataService>;

  beforeEach(() => {
    dataSpy = jasmine.createSpyObj('DataService', ['get']);

    TestBed.configureTestingModule({
      providers: [
        SearchService,
        { provide: DataService, useValue: dataSpy },
      ],
    });

    service = TestBed.inject(SearchService);
  });

  it('Should make a get call on get search call', () => {
    const responseData = { 'data': [] };
    dataSpy.get.and.returnValue(of(responseData));

    const actual = service.get("searching_text");

    expect(dataSpy.get).toHaveBeenCalledOnceWith('search/searching_text');

    actual.subscribe(res => {
      expect(res).toBe(responseData);
    })
  });
});
