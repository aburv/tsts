import { TestBed } from '@angular/core/testing';
import { UserButtonComponent } from './user-button.component';
import { UserDataService } from 'src/app/_services/UserData.service';
import { AuthUserService } from 'src/app/_services/auth-user.service';
import { DeviceService } from 'src/app/_services/device.service';
import { of } from 'rxjs';
import { AppUser, GAuthUser } from '../../_models/user';
import { Icon } from '../icon/icon.component';
import { Config } from 'src/app/config';
import { By } from '@angular/platform-browser';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('UserButtonComponent', () => {

  const authUserService = jasmine.createSpyObj('AuthUserService', [
    'handleGoogleResponse',
    'getLoggedUser'
  ]);
  authUserService.getLoggedUser.and.returnValue(of());

  const userDataService = jasmine.createSpyObj('UserDataService', [
    'signIn',
    'getUser',
    'autoSignIn'
  ]);

  let deviceService: jasmine.SpyObj<DeviceService>;

  beforeAll(() => {
    deviceService = jasmine.createSpyObj('DeviceService', ['getDeviceId', 'getValues']);
  });

  beforeEach(async () => {
    deviceService.getDeviceId.and.returnValue('test-device-id');
    deviceService.getValues.and.returnValue({ id: 'test-device-id' });

    const googleSpy = {
      initialize: jasmine.createSpy('initialize'),
      renderButton: jasmine.createSpy('renderButton'),
      prompt: jasmine.createSpy('prompt'),
    };
    (window as any).google = {
      accounts: {
        id: googleSpy
      }
    };

    await TestBed.configureTestingModule({
      imports: [UserButtonComponent, HttpClientTestingModule],
      providers: [
        {
          provide: AuthUserService,
          useValue: authUserService
        },
        {
          provide: UserDataService,
          useValue: userDataService
        },
        {
          provide: DeviceService,
          useValue: deviceService
        },
      ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA]
    })
      .compileComponents();
  });

  beforeEach(() => {
    userDataService.autoSignIn.calls.reset();
    authUserService.getLoggedUser.calls.reset();
    userDataService.signIn.calls.reset();
    userDataService.getUser.calls.reset();
    deviceService.getDeviceId.calls.reset();
    deviceService.getValues.calls.reset();
    
    userDataService.autoSignIn.and.returnValue(of(false));
    authUserService.getLoggedUser.and.returnValue(of());
    deviceService.getDeviceId.and.returnValue('test-device-id');
    deviceService.getValues.and.returnValue({ id: 'test-device-id' });
  });

  it('Should create', () => {
    const fixture = TestBed.createComponent(UserButtonComponent);
    const component = fixture.componentInstance;

    expect(component).toBeTruthy();
  });

  it('Should start listening to loggedIn User with login and autoSignIn with setcurrentuser if there is user on ngInit', () => {
    const fixture = TestBed.createComponent(UserButtonComponent);
    const component = fixture.componentInstance;

    const userLoginSpy = spyOn(component, 'userLogin');
    const setCurrentUserSpy = spyOn(component, 'setCurrentUser');

    const mockedGAuthUser: GAuthUser = {
      sub: "id",
      email: "email",
      name: "name",
      picture: "photoUrl",
      firstName: '',
      lastName: ''
    };

    userDataService.autoSignIn.and.returnValue(of(true));
    authUserService.getLoggedUser.and.returnValue(of(mockedGAuthUser));

    component.ngOnInit();

    expect(userDataService.autoSignIn).toHaveBeenCalledOnceWith();

    expect(authUserService.getLoggedUser).toHaveBeenCalledOnceWith();
    expect(userLoginSpy).toHaveBeenCalledOnceWith(mockedGAuthUser);
    expect(setCurrentUserSpy).toHaveBeenCalledOnceWith();

    userLoginSpy.calls.reset();
    setCurrentUserSpy.calls.reset();
  });

  it('Should start listening to loggedIn User and init google signOn if there is no user on ngInit', () => {
    const fixture = TestBed.createComponent(UserButtonComponent);
    const component = fixture.componentInstance;

    const userLoginSpy = spyOn(component, 'userLogin');
    const initializeGoogleSignInSpy = spyOn(component, 'initializeGoogleSignIn');

    authUserService.getLoggedUser.and.returnValue(of(null));

    userDataService.autoSignIn.and.returnValue(of(false));

    component.ngOnInit();

    expect(userDataService.autoSignIn).toHaveBeenCalledOnceWith();

    expect(authUserService.getLoggedUser).toHaveBeenCalledOnceWith();
    expect(initializeGoogleSignInSpy).toHaveBeenCalledOnceWith();

    userLoginSpy.calls.reset();
    initializeGoogleSignInSpy.calls.reset();
  });

  it('Should initialize Google Sign-In, render button, and prompt One Tap', () => {
    const fixture = TestBed.createComponent(UserButtonComponent);
    const component = fixture.componentInstance;

    const container = fixture.debugElement.query(By.css('#google-signin-button')).nativeElement as HTMLElement;
    spyOn(Config, 'getGCID').and.returnValue('GClientId');

    component.initializeGoogleSignIn();

    const initialize = (window as any).google.accounts.id.initialize;
    expect(initialize).toHaveBeenCalledWith({
      client_id: 'GClientId',
      callback: jasmine.any(Function)
    });

    const mockResponse = { credential: 'mock-token' };
    const callback = initialize.calls.argsFor(0)[0].callback;
    callback(mockResponse);

    expect(authUserService.handleGoogleResponse).toHaveBeenCalledWith(mockResponse);

    expect(google.accounts.id.renderButton).toHaveBeenCalledWith(container, {
      type: 'icon',
      theme: 'outline',
      size: 'large',
      shape: 'pill',
    });

    expect(google.accounts.id.prompt).toHaveBeenCalled();

  });

  it('Should set on setLocation', () => {
    const fixture = TestBed.createComponent(UserButtonComponent);
    const component = fixture.componentInstance;

    const mockPosition: GeolocationPosition = {
      coords: {
        latitude: 51.5074,
        longitude: 0.1278,
        accuracy: 100,
        altitude: 0,
        altitudeAccuracy: 0,
        heading: 0,
        speed: 0,
        toJSON: () => ({})
      },
      timestamp: Date.now(),
      toJSON: () => ({})
    };

    expect(component.location).toBe(null);

    component.setLocation(mockPosition);

    expect(component.location).toEqual({
      long: 0.1278,
      lat: 51.5074
    });
  });

  it('Should make callback to setLocation on getLocation', () => {
    const fixture = TestBed.createComponent(UserButtonComponent);
    const component = fixture.componentInstance;

    const mockPosition: GeolocationPosition = {
      coords: {
        latitude: 51.5074,
        longitude: 0.1278,
        accuracy: 100,
        altitude: 0,
        altitudeAccuracy: 0,
        heading: 0,
        speed: 0,
        toJSON: () => ({})
      },
      timestamp: Date.now(),
      toJSON: () => ({})
    };

    spyOn(component, 'setLocation');
    spyOn(navigator.geolocation, 'getCurrentPosition').and.callFake((success: any) => {
      success(mockPosition);
    });

    component.getLocation();

    expect(component.setLocation).toHaveBeenCalledOnceWith(mockPosition);
  });

  it('Should make a login call set user on userLogin', () => {
    const fixture = TestBed.createComponent(UserButtonComponent);
    const component = fixture.componentInstance;

    userDataService.signIn.and.returnValue(of(true));

    spyOn(component, 'getLocation');
    spyOn(component, 'setCurrentUser');
    const userMock = jasmine.createSpyObj('AuthUtils', ["decodeJwt"]);
    userMock.sub = "id";
    userMock.email = "email";
    userMock.name = "name";
    userMock.picture = "photoUrl";

    component.userLogin(userMock);

    expect(component.getLocation).toHaveBeenCalledOnceWith();
    expect(userDataService.signIn).toHaveBeenCalledOnceWith(
      {
        user: {
          uId: { gId: 'id', value: 'email', type: 'M' },
          name: "name",
          picUrl: 'photoUrl'
        },
        login: { deviceId: 'test-device-id', location: null }
      },
    );

    expect(component.setCurrentUser).toHaveBeenCalledOnceWith();
    expect(component.getLocation).toHaveBeenCalledOnceWith();
  });

  it('Should get and set user on setCurrentUser', () => {
    const fixture = TestBed.createComponent(UserButtonComponent);
    const component = fixture.componentInstance;

    const googleButton = fixture.debugElement.query(By.css('#google-signin-button'));

    expect(googleButton.styles['visibility']).toBe('');

    userDataService.getUser.and.returnValue({ dp: "dp", name: "name", email: "email" });

    component.setCurrentUser();

    expect(userDataService.getUser).toHaveBeenCalledOnceWith();
    expect(component.user).toEqual({ dp: "dp", name: "name", email: "email" });

    expect(googleButton.styles['visibility']).toBe('hidden');
  });

  it('View: Should set the content on no user', () => {
    userDataService.autoSignIn.and.returnValue(of(""));

    const fixture = TestBed.createComponent(UserButtonComponent);
    const component = fixture.componentInstance;

    component.user = null;
    component.isDialogOn = false;

    fixture.detectChanges();

    const googleButton = fixture.debugElement.query(By.css('#google-signin-button'));
    const dialogElement = fixture.debugElement.query(By.css('app-dialog'));
    const imageElements = fixture.debugElement.queryAll(By.css('app-image'));

    expect(googleButton).not.toBeNull();
    expect(googleButton.nativeElement.id).toBe('google-signin-button');
    expect(dialogElement).toBeNull();
    expect(imageElements.length).toBe(0);
  });

  it('View: Should set the content on user with no dialog', () => {
    userDataService.autoSignIn.and.returnValue(of(""));

    const fixture = TestBed.createComponent(UserButtonComponent);
    const component = fixture.componentInstance;

    component.user = {
      dp: "dp", name: "name", email: "email"
    };

    component.isDialogOn = false;

    fixture.detectChanges();

    const googleElement = fixture.debugElement.query(By.css('div'));
    const imageElement = fixture.debugElement.query(By.css('app-image'));
    const dialogElement = fixture.debugElement.query(By.css('app-dialog'));

    expect(fixture.debugElement.children.length).toBe(2);

    expect(googleElement.nativeElement.id).toBe('google-signin-button');

    expect(imageElement.componentInstance.icon()).toBe(Icon.PERSON);
    expect(imageElement.componentInstance.id()).toBe('dp');

    expect(dialogElement).toBeNull();
  });

  it('View: Should set the content on user with dialog', () => {
    userDataService.autoSignIn.and.returnValue(of(""));

    const fixture = TestBed.createComponent(UserButtonComponent);
    const component = fixture.componentInstance;

    component.user = {
      dp: "dp", name: "name", email: "email"
    };

    component.isDialogOn = true;

    fixture.detectChanges();

    const googleElement = fixture.debugElement.query(By.css('div'));
    const imageElement = fixture.debugElement.query(By.css('app-image'));
    const dialogElement = fixture.debugElement.query(By.css('app-dialog'));

    expect(fixture.debugElement.children.length).toBe(3);

    expect(googleElement.nativeElement.id).toBe('google-signin-button');

    expect(imageElement.componentInstance.icon()).toBe(Icon.PERSON);
    expect(imageElement.componentInstance.id()).toBe('dp');

    expect(dialogElement).toBeTruthy();
  });

  it('View: Should set dialog', () => {
    userDataService.autoSignIn.and.returnValue(of(""));

    const fixture = TestBed.createComponent(UserButtonComponent);
    const component = fixture.componentInstance;

    component.user = {
      dp: "dp", name: "name", email: "email"
    };

    component.isDialogOn = true;

    fixture.detectChanges();

    const googleElement = fixture.debugElement.query(By.css('div'));
    const imageElement = fixture.debugElement.query(By.css('app-image'));
    const dialogElement = fixture.debugElement.query(By.css('app-dialog'));

    expect(fixture.debugElement.children.length).toBe(3);

    expect(googleElement.nativeElement.id).toBe('google-signin-button');

    expect(imageElement.componentInstance.icon()).toBe(Icon.PERSON);
    expect(imageElement.componentInstance.id()).toBe('dp');

    expect(dialogElement).toBeTruthy();
  });

  it('View: Should turn dialog display when clicked on user with no dialog', () => {
    userDataService.autoSignIn.and.returnValue(of(""));

    const fixture = TestBed.createComponent(UserButtonComponent);
    const component = fixture.componentInstance;

    component.user = {
      dp: "dp", name: "name", email: "email"
    };

    component.isDialogOn = false;

    fixture.detectChanges();

    const googleElement = fixture.debugElement.query(By.css('div'));
    const imageElement = fixture.debugElement.query(By.css('app-image'));
    const dialogElement = fixture.debugElement.query(By.css('app-dialog'));

    expect(fixture.debugElement.children.length).toBe(2);

    expect(googleElement.nativeElement.id).toBe('google-signin-button');

    expect(imageElement.componentInstance.icon()).toBe(Icon.PERSON);
    expect(imageElement.componentInstance.id()).toBe('dp');

    expect(component.isDialogOn).toBeFalse();
    expect(dialogElement).toBeNull();

    imageElement.nativeElement.click();

    expect(component.isDialogOn).toBeTrue();
  });
});
