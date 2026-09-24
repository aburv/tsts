import { of } from "rxjs";
import { PlayerService } from "./player.service";
import { DataService } from "./data.service";
import { TestBed } from "@angular/core/testing";

describe('Player Service', () => {
    let service: PlayerService;
    let dataSpy: jasmine.SpyObj<DataService>;

    beforeEach(() => {
        dataSpy = jasmine.createSpyObj('DataService', ['get', 'post']);

        TestBed.configureTestingModule({
            providers: [
                PlayerService,
                { provide: DataService, useValue: dataSpy },
            ],
        });

        service = TestBed.inject(PlayerService);
    });


    it('Should get player basic info by id on getInfo call', () => {
        const responseData = { 'data': [] };
        dataSpy.get.and.returnValue(of(responseData));

        const actual = service.getInfo("playerId");

        expect(dataSpy.get).toHaveBeenCalledOnceWith('player/playerId');

        actual.subscribe((res: any) => {
            expect(res).toBe(responseData);
        });
    });

});
