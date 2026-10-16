import { of } from 'rxjs';
import { TestBed } from '@angular/core/testing';
import { UserService } from './user.service';
import { DataService } from './data.service';

describe('UserService', () => {
  let service: UserService;
  let dataSpy: jasmine.SpyObj<DataService>;

  beforeEach(() => {
    dataSpy = jasmine.createSpyObj('DataService', ['get']);

    TestBed.configureTestingModule({
      providers: [
        UserService,
        { provide: DataService, useValue: dataSpy },
      ],
    });

    service = TestBed.inject(UserService);
  });

  it('Should make a get call on getUserData call', () => {
    const responseData = { data: [] };
    dataSpy.get.and.returnValue(of(responseData));

    const actual = service.getUserData();

    expect(dataSpy.get).toHaveBeenCalledOnceWith('user/app');

    actual.subscribe((res) => {
      expect(res).toBe(responseData);
    });
  });
});
