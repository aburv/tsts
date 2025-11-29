import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { PlayerComponent } from './player.component';
import { ActivatedRoute, Router } from '@angular/router';
import { LoaderService } from 'src/app/_services/loader.service';
import { PlayerService } from 'src/app/_services/player.service';
import { of } from 'rxjs';
import { UserDataService } from 'src/app/_services/UserData.service';

describe('PlayerComponent', () => {
  let component: PlayerComponent;
  let fixture: ComponentFixture<PlayerComponent>;

  const userService = jasmine.createSpyObj('UserDataService', [
    'getMyPlayerId'
  ]);
  userService.getMyPlayerId.and.returnValue('id');

  const playerService = jasmine.createSpyObj('PlayerService', [
    'getInfo',
  ]);

  const loaderService = jasmine.createSpyObj('LoaderService', ['loadingOn', 'loadingOff']);

  const router = { navigate: jasmine.createSpy('navigate') };

  const activatedRoute = { params: of({ id: 'id' }) };

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PlayerComponent],
      providers: [
        { provide: Router, useValue: router },
        { provide: ActivatedRoute, useValue: activatedRoute },
        { provide: LoaderService, useValue: loaderService },
        { provide: PlayerService, useValue: playerService },
        { provide: UserDataService, useValue: userService },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(PlayerComponent);
    component = fixture.componentInstance;

    userService.getMyPlayerId.calls.reset();
    playerService.getInfo.calls.reset();
  });

  it('Should create the component', () => {
    expect(component).toBeTruthy();
  });

  it('Should call getInfo with i am player on init', () => {
    playerService.getInfo.and.returnValue(of({
      data: {
        name: "player 1",
        dp: "",
        location: "location",
        height: "20",
        weight: "70",
        age: "25",
        positions: []
      }
    }));
    
    const generateTabSpy = spyOn(component, 'generateTab');
    const getMyPlayerIdSpy = spyOn(component, 'isMyPlayerProfile').and.returnValue(true);

    component.ngOnInit();

    expect(playerService.getInfo).toHaveBeenCalledOnceWith('id');
    expect(generateTabSpy).toHaveBeenCalled();
    expect(getMyPlayerIdSpy).toHaveBeenCalled();

    generateTabSpy.calls.reset();
    getMyPlayerIdSpy.calls.reset();
  });

  it('Should call getInfo with i am not player on init', () => {
    playerService.getInfo.and.returnValue(of({
      data: {
        name: "player 1",
        dp: "",
        location: "location",
        height: "20",
        weight: "70",
        age: "25",
        positions: []
      }
    }));

    const generateTabSpy = spyOn(component, 'generateTab');
    const getMyPlayerIdSpy = spyOn(component, 'isMyPlayerProfile').and.returnValue(false);

    component.ngOnInit();

    expect(playerService.getInfo).toHaveBeenCalledOnceWith('id');
    expect(generateTabSpy).toHaveBeenCalled();
    expect(getMyPlayerIdSpy).toHaveBeenCalled();

    generateTabSpy.calls.reset();
    getMyPlayerIdSpy.calls.reset();
  });

  it('Should return true if playerId is same as my playerId on ', () => {
    component.id = "player_id";
    userService.getMyPlayerId.and.returnValue("player_id");

    const actual = component.isMyPlayerProfile();

    expect(actual).toBeTrue()
    expect(userService.getMyPlayerId).toHaveBeenCalledOnceWith()
  });

  it('Should return true if playerId is same as my playerId on ', () => {
    component.id = "player_id";
    userService.getMyPlayerId.and.returnValue("player_different_id");

    const actual = component.isMyPlayerProfile();

    expect(actual).toBeFalse()
    expect(userService.getMyPlayerId).toHaveBeenCalledOnceWith()
  });

  it('Should set selectedTabIndex on onTabSelect', () => {
    component.onTabSelect(1);
    expect(component.selectedTabIndex()).toBe(1);
    component.onTabSelect(0);
    expect(component.selectedTabIndex()).toBe(0);
  });

  it('Should generate tabs correctly', () => {
    component.tabContent = ['Overview'];
    component.generateTab();
    const tabs = component.tabContent;
    expect(tabs).toContain('Stats');
    expect(tabs).toContain('Timeline');
  });

  it('View: Should render player banner with correct info', () => {
    fixture.detectChanges();
    component.player = {
      name: 'John Doe',
      dp: 'path/to/photo.jpg',
      positions: ['Forward', 'Midfielder'],
      location: 'New York',
      age: "25",
      height: "180",
      weight: "75"
    };

    fixture.detectChanges();

    const nameEl = fixture.debugElement.query(By.css('.player-name')).nativeElement;
    expect(nameEl.textContent).toContain('John Doe');

    const imgEl = fixture.debugElement.query(By.css('img')).nativeElement;
    expect(imgEl.src).toContain('path/to/photo.jpg');

    const positionsEl = fixture.debugElement.query(By.css('.sub')).nativeElement;
    expect(positionsEl.textContent).toContain('Forward, Midfielder');

    const locationEl = fixture.debugElement.query(By.css('.details div:nth-child(2)')).nativeElement;
    expect(locationEl.textContent).toContain('New York');

    const ageEl = fixture.debugElement.query(By.css('.bio div:nth-child(1) b')).nativeElement;
    expect(ageEl.textContent).toContain('25');
    const heightEl = fixture.debugElement.query(By.css('.bio div:nth-child(2) b')).nativeElement;
    expect(heightEl.textContent).toContain('180');
    const weightEl = fixture.debugElement.query(By.css('.bio div:nth-child(3) b')).nativeElement;
    expect(weightEl.textContent).toContain('75');
  });

  it('View: Should render tabs if multiple tabContent exists', () => {
    fixture.detectChanges();
    component.player = {
      name: 'John Doe',
      dp: 'path/to/photo.jpg',
      positions: ['Forward', 'Midfielder'],
      location: 'New York',
      age: "25",
      height: "180",
      weight: "75"
    };

    component.tabContent = ['Profile', 'Stats', 'Tournaments'];

    fixture.detectChanges();

    const tabs = fixture.debugElement.queryAll(By.css('.tab'));
    expect(tabs.length).toBe(3);
    expect(tabs[0].nativeElement.textContent).toContain('Profile');
    expect(tabs[1].nativeElement.textContent).toContain('Stats');
    expect(tabs[2].nativeElement.textContent).toContain('Tournaments');
  });

  it('View: Should call onTabSelect when tab clicked', () => {
    fixture.detectChanges();
    component.player = {
      name: 'John Doe',
      dp: 'path/to/photo.jpg',
      positions: ['Forward', 'Midfielder'],
      location: 'New York',
      age: "25",
      height: "180",
      weight: "75"
    };;
    component.tabContent = ['Profile', 'Stats'];
    spyOn(component, 'onTabSelect');
    fixture.detectChanges();

    const tabs = fixture.debugElement.queryAll(By.css('.tab'));

    tabs[1].triggerEventHandler('click', null);

    expect(component.onTabSelect).toHaveBeenCalledWith(1);
  });

  it('View: Should render empty container for tab 0', () => {
    component.player = {
      name: 'John Doe',
      dp: 'path/to/photo.jpg',
      positions: ['Forward', 'Midfielder'],
      location: 'New York',
      age: "25",
      height: "180",
      weight: "75"
    };
    component.selectedTabIndex.set(0);

    fixture.detectChanges();

    const container = fixture.debugElement.query(By.css('.container.scrollable'));
    expect(container).toBeTruthy();
  });

  it('View: Should show warning if player not found', () => {
    fixture.detectChanges();
    component.player = null;

    fixture.detectChanges();

    const warningEl = fixture.debugElement.query(By.css('.warning-layout p')).nativeElement.textContent;
    expect(warningEl).toContain('Player not found');
  });
});
