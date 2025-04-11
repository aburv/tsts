import { TestBed, fakeAsync, flush, tick } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { AppComponent } from './app.component';
import { Router } from '@angular/router';
import { ThemeService } from './_services/theme.service';
import { UserService } from './_services/user.service';
import { of, throwError } from 'rxjs';
import { CUSTOM_ELEMENTS_SCHEMA, signal } from '@angular/core';
import { By } from '@angular/platform-browser';
import { LoaderService } from './_services/loader.service';
import { PingService } from './_services/ping.service';
import { DeviceService } from './_services/device.service';
import { SearchService } from './_services/search.service';
import { Config } from './config';

describe('AppComponent', () => {
  const userService = jasmine.createSpyObj('UserService', [
    'getUserData'
  ]);
  userService.getUserData.and.returnValue(of({ data: {} }));

  const deviceService = jasmine.createSpyObj('DeviceService', [
    'sendDeviceDetails'
  ]);
  deviceService.sendDeviceDetails.and.returnValue()

  const searchService = jasmine.createSpyObj('SearchService', [
    'get'
  ]);
  searchService.get.and.returnValue(of({ data: [] }))

  const pingService = jasmine.createSpyObj('PingService', [
    'ping',
  ]);
  pingService.ping.and.returnValue(of(''));

  const loaderService = jasmine.createSpyObj('LoaderService', ['getIsLoading']);

  const themeService = jasmine.createSpyObj('ThemeService', [
    'initTheme',
    'setTheme',
  ]);
  themeService.initTheme.and.returnValue(null);
  themeService.setTheme.and.returnValue(null);

  const router = {
    navigate: jasmine.createSpy('navigate'),
  };

  beforeEach(() => TestBed.configureTestingModule({
    imports: [RouterTestingModule],
    providers: [
      {
        provide: Router,
        useValue: router,
      },
      {
        provide: ThemeService,
        useValue: themeService,
      },
      {
        provide: UserService,
        useValue: userService,
      },
      {
        provide: DeviceService,
        useValue: deviceService
      },
      {
        provide: SearchService,
        useValue: searchService
      },
      {
        provide: LoaderService,
        useValue: loaderService,
      },
      {
        provide: PingService,
        useValue: pingService,
      }
    ],
    declarations: [AppComponent],
    schemas: [CUSTOM_ELEMENTS_SCHEMA]
  }));

  beforeEach(() => {
    userService.getUserData.calls.reset();
    deviceService.sendDeviceDetails.calls.reset();
    themeService.initTheme.calls.reset();
    themeService.setTheme.calls.reset();
    LoaderService.status.set(false);
    PingService.isServerDown.set(false);

    spyOn(Config, "getSiteDomain").and.returnValue("https://host")
  });

  it('Should create the app on success loading data', fakeAsync(() => {
    class Media implements MediaQueryList {
      matches = true;
      media = '';
      onchange: ((this: MediaQueryList, ev: MediaQueryListEvent) => any) | null = null;
      addListener(callback: ((this: MediaQueryList, ev: MediaQueryListEvent) => any) | null): void { return }
      removeListener(callback: ((this: MediaQueryList, ev: MediaQueryListEvent) => any) | null): void { return }
      addEventListener<K extends 'change'>(type: K, listener: (this: MediaQueryList, ev: MediaQueryListEventMap[K]) => any, options?: boolean | AddEventListenerOptions | undefined): void;
      addEventListener(type: string, listener: EventListenerOrEventListenerObject, options?: boolean | AddEventListenerOptions | undefined): void;
      addEventListener(type: unknown, listener: unknown, options?: unknown): void { return }
      removeEventListener<K extends 'change'>(type: K, listener: (this: MediaQueryList, ev: MediaQueryListEventMap[K]) => any, options?: boolean | EventListenerOptions | undefined): void;
      removeEventListener(type: string, listener: EventListenerOrEventListenerObject, options?: boolean | EventListenerOptions | undefined): void;
      removeEventListener(type: unknown, listener: unknown, options?: unknown): void { return }
      dispatchEvent(event: Event): boolean {
        return false;
      }
    }
    const media = new Media()
    spyOn(window, 'matchMedia').and.returnValue(media);

    spyOn(media, 'addEventListener');

    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;

    expect(app).toBeTruthy();

    expect(app.isInInit).toBe(true);
    expect(userService.getUserData).toHaveBeenCalledOnceWith();
    expect(deviceService.sendDeviceDetails).toHaveBeenCalledOnceWith();
    expect(themeService.initTheme).toHaveBeenCalledOnceWith(true);
    expect(window.matchMedia).toHaveBeenCalledOnceWith("(prefers-color-scheme: dark)");

    themeService.initTheme.calls.reset();

    tick(1100);

    expect(app.isInInit).toBe(false);

    expect(media.addEventListener).toHaveBeenCalledWith('change', jasmine.any(Function))
  }));

  it('Should set the isLoading to true on call', () => {
    LoaderService.status.set(true);

    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;

    expect(app.isLoading()).toBe(true);
  });

  it('Should set the isLoading false on call', () => {
    LoaderService.status.set(false);

    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;

    expect(app.isLoading()).toBe(false);
  });

  it('Should create the app on failure loading data', fakeAsync(() => {
    userService.getUserData.and.returnValue(throwError(''));

    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;

    expect(app).toBeTruthy();

    expect(app.isInInit).toBe(true);
    expect(userService.getUserData).toHaveBeenCalledOnceWith();

    themeService.initTheme.calls.reset();

    tick(1100);

    expect(app.isInInit).toBe(false);

    userService.getUserData.calls.reset();
  }));

  it('Should set search text and make a get call on onChange call', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;

    app.onChange({ target: { value: 'value' } });

    expect(app.searchText()).toBe('value')
    expect(searchService.get).toHaveBeenCalledOnceWith('value')
    searchService.get.calls.reset()
  });

  it('Should set search text on onChange call', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;

    app.onChange({ target: { value: '' } });

    expect(app.searchText()).toBe('')
    expect(searchService.get).not.toHaveBeenCalled()
    searchService.get.calls.reset()
  });

  it('Should set isSearching to true and focus on searchInput on turnToSearching call', fakeAsync(() => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    app.searchInput = {
      nativeElement: jasmine.createSpyObj('nativeElement', ['focus'])
    }
    app.isSearching = false;

    app.turnToSearching();

    expect(app.isSearching).toBe(true);
    tick(500);
    expect(app.searchInput.nativeElement.focus).toHaveBeenCalled();
    flush();
  }));

  it('Should set nothing on turnToSearching call', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    app.isSearching = true;

    app.turnToSearching();

    expect(app.isSearching).toBe(true);
  });

  it('Should set search text to empty and isSearching to false on onSearchClose call', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    app.isSearching = true;

    app.onSearchClose();

    expect(app.searchText()).toBe('');
    expect(app.isSearching).toBe(false);
  });

  it('Should navigate to dashboard', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;

    app.navigateToDashboard();

    expect(router.navigate).toHaveBeenCalledOnceWith(['home']);
  });

  it('View: Should set root with screen and layout classes and its children', fakeAsync(() => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;

    fixture.detectChanges();

    const root = fixture.debugElement.query(By.css('div'));

    expect(root.classes['screen']).toBe(true);
    expect(root.classes['layout']).toBe(true);

    expect(root.children.length).toBe(3);

    expect(root.children[0].classes['splash-layout']).toBe(true);
    expect(root.children[1].classes['app-support-layout']).toBe(true);
    expect(root.children[2].classes['footer-layout']).toBe(true);

    expect(root.children[0].children.length).toBe(1);
    expect(root.children[0].children[0].children.length).toBe(2);
    const img = root.children[0].children[0].query(By.css('img'));

    expect(root.children[0].children[0].children[0]).toEqual(img);
    expect(root.children[0].children[0].children[0].classes['loader']).toBe(true);
    expect(img.attributes['src']).toBe('../assets/logo_app_164.png');
    expect(root.children[0].children[0].children[1].nativeElement.textContent).toBe('Takbuff');
    expect(root.children[0].children[0].children[1].styles['text-align']).toBe('center');
    expect(root.children[0].children[0].children[1].styles['font-size']).toEqual('30px');

    tick(1100);
    fixture.detectChanges();

    expect(root.children.length).toBe(3);
    expect(root.children[0].classes['content']).toBe(true);
    expect(root.children[1].classes['app-support-layout']).toBe(true);
    expect(root.children[2].classes['footer-layout']).toBe(true);

    const icon = root.children[1].queryAll(By.css('app-icon'));
    const breakLine = root.children[1].query(By.css('br'));
    expect(root.children[1].children.length).toBe(3);
    expect(root.children[1].children[0]).toBe(icon[0]);
    expect(icon[0].attributes['name']).toBe('android');
    expect(icon[0].nativeElement.size).toBe(30);
    expect(root.children[1].children[1]).toBe(breakLine);
    expect(root.children[1].children[2]).toBe(icon[1]);
    expect(icon[1].attributes['name']).toBe('ios');
    expect(icon[1].nativeElement.size).toBe(30);


    expect(root.children[2].children.length).toBe(1);
    expect(root.children[2].children[0].classes['footer']).toBe(true);
    expect(root.children[2].children[0].children.length).toBe(2);
    expect(root.children[2].children[0].children[0].classes['links']).toBe(true);
    expect(root.children[2].children[0].children[0].classes['bottom']).toBe(true);
    expect(root.children[2].children[0].children[0].children.length).toBe(app.links.length);

    for (let i = 0; i < root.children[2].children[0].children[0].children.length; i++) {
      expect(root.children[2].children[0].children[0].children[i].children[0].nativeElement.textContent).toBe(" " + app.links[i].title + " ");
      if (i !== app.links.length - 1) {
        expect(root.children[2].children[0].children[0].children[i].children[1].nativeElement.textContent).toBe("|");
      }
      expect(root.children[2].children[0].children[0].children[i].children[0].classes['link']).toBe(true);
      expect(root.children[2].children[0].children[0].children[i].children[0].attributes['href']).toBe('https://host' + app.links[i].link);
      expect(root.children[2].children[0].children[0].children[i].children[0].attributes['target']).toBe('_blank');
    }
    expect(root.children[2].children[0].children[1].children.length).toBe(3);
    expect(root.children[2].children[0].children[1].children[0].nativeElement.textContent).toBe('Powered by Aburv | Takbuff © 2025');
    expect(root.children[2].children[0].children[1].children[1].attributes['class']).toBe('break');
    expect(root.children[2].children[0].children[1].children[2].nativeElement.textContent).toBe(' An Open Source Application');
    expect(root.children[2].children[0].children[1].children[2].styles["font-size"]).toBe('12px');
  }));

  it('View: Should set content and its children', fakeAsync(() => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;

    spyOn(app, 'navigateToDashboard')
    spyOn(app, 'turnToSearching')
    spyOn(app, 'onSearchClose')
    spyOn(app, 'onChange')

    tick(1100);
    fixture.detectChanges();

    const root = fixture.debugElement.query(By.css('div'));

    expect(root.children.length).toBe(3);
    expect(root.children[0].classes['content']).toBe(true);
    expect(root.children[0].children.length).toBe(2);
    expect(root.children[0].children[0].classes['header-layout']).toBe(true);
    expect(root.children[0].children[0].children.length).toBe(3);
    expect(root.children[0].children[0].children[0].classes['title']).toBe(true);
    root.children[0].children[0].children[0].triggerEventHandler('click');
    expect(app.navigateToDashboard).toHaveBeenCalledOnceWith();
    expect(root.children[0].children[0].children[0].children.length).toBe(2);
    const img = root.children[0].children[0].children[0].query(By.css('img'));
    const bold = root.children[0].children[0].children[0].query(By.css('b'));
    expect(root.children[0].children[0].children[0].children[0]).toBe(img);
    expect(img.attributes['src']).toBe('../assets/logo_app_164.png');
    expect(root.children[0].children[0].children[0].children[1]).toBe(bold);
    expect(bold.nativeElement.textContent).toBe('Takbuff');

    expect(root.children[0].children[0].children[1].classes['spacer']).toBe(true);

    expect(root.children[0].children[0].children[2].classes['search']).toBe(true);
    expect(root.children[0].children[0].children[2].children.length).toBe(2);

    let icon = root.children[0].children[0].children[2].queryAll(By.css('app-icon'));
    const input = root.children[0].children[0].children[2].query(By.css('input'));
    expect(root.children[0].children[0].children[2].children[0]).toBe(icon[0]);
    expect(icon[0].attributes['name']).toBe('search');
    expect(icon[0].nativeElement.size).toBe(30);
    expect(icon[0].styles['cursor']).toBe('pointer');
    expect(root.children[0].children[0].children[2].children[1]).toEqual(input);
    expect(input.attributes['placeholder']).toBe('Search here');
    expect(input.nativeElement.value).toBe('');

    expect(root.children[0].children[1].classes['layout']).toBe(true);
    expect(root.children[0].children[1].children.length).toBe(3);
    expect(root.children[0].children[1].children[0].classes['side-bar-layout']).toBe(true);
    expect(root.children[0].children[1].children[1].classes['main-layout']).toBe(true);
    expect(root.children[0].children[1].children[1].children.length).toBe(1);
    const router = root.children[0].children[1].children[1].query(By.css('router-outlet'))
    expect(root.children[0].children[1].children[1].children[0]).toBe(router);
    expect(root.children[0].children[1].children[2].children[0].classes['side-bar-layout']).toBe(true);

    icon[0].triggerEventHandler('click');
    expect(app.turnToSearching).toHaveBeenCalledOnceWith();
    app.searchText.set('value')
    const result = ['']
    app.searchResult = result;

    app.isSearching = true;

    fixture.detectChanges();

    expect(root.children[0].children[0].children[2].children.length).toBe(3);
    icon = root.children[0].children[0].children[2].queryAll(By.css('app-icon'));
    expect(root.children[0].children[0].children[2].children[0]).toBe(icon[0]);
    expect(icon[0].styles['cursor']).toBe('default');
    expect(root.children[0].children[0].children[2].children[2]).toBe(icon[1]);
    expect(icon[1].attributes['name']).toBe('cross');
    expect(icon[1].nativeElement.size).toBe(20);
    expect(icon[1].styles['cursor']).toBe('pointer');
    expect(app.searchText()).toBe('value');
    icon[1].triggerEventHandler('click');
    expect(app.onSearchClose).toHaveBeenCalledOnceWith();

    expect(root.children[0].children[0].children[2].children[1].classes['disp-input']).toBe(true);

    input.triggerEventHandler('keyup', { target: { value: '' } });
    expect(app.onChange).toHaveBeenCalledOnceWith({ target: { value: '' } });

    expect(root.children[0].children[1].children[1].classes['main-layout']).toBe(true);
    expect(root.children[0].children[1].children[1].children.length).toBe(result.length);
    for (let i = 0; i < result.length; i++) {
      expect(root.children[0].children[1].children[1].children[i].classes['search-result-item']).toBe(true);
    }
    flush();
  }));

  it('View: Should set loading layout', fakeAsync(() => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;

    tick(1100);

    LoaderService.status.set(true);

    fixture.detectChanges();

    const root = fixture.debugElement.query(By.css('div'));

    expect(root.children.length).toBe(4);
    expect(root.children[0].classes['content']).toBe(true);
    expect(root.children[1].classes['app-support-layout']).toBe(true);
    expect(root.children[2].classes['footer-layout']).toBe(true);
    expect(root.children[3].classes['loader-layout']).toBe(true);

    expect(root.children[3].children.length).toBe(1);
    const img = root.children[3].query(By.css('img'));
    expect(root.children[3].children[0]).toEqual(img);
    expect(root.children[3].children[0].classes['loader']).toBe(true);
    expect(img.attributes['src']).toBe('../assets/logo_app_164.png');

  }));

  it('View: Should set links below the right side layout', fakeAsync(() => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;

    tick(1100);

    LoaderService.status.set(true);

    fixture.detectChanges();

    const root = fixture.debugElement.query(By.css('div'));

    expect(root.children[0].children[1].children[2].children[1].classes['links']).toBe(true);
    expect(root.children[0].children[1].children[2].children[1].classes['side']).toBe(true);

    expect(root.children[0].children[1].children[2].children[1].children.length).toBe(app.links.length);

    expect(root.children[0].children[1].children[2].children[1].children.length).toBe(app.links.length);
    for (let i = 0; i < root.children[0].children[1].children[2].children[1].children.length; i++) {
      expect(root.children[0].children[1].children[2].children[1].children[i].children[0].nativeElement.textContent).toBe(" " + app.links[i].title + " ");
      if (i === 0 || i === 1 || i === 3 || i === 4) {
        expect(root.children[0].children[1].children[2].children[1].children[i].children[1].nativeElement.textContent).toBe("|");
      }
      expect(root.children[0].children[1].children[2].children[1].children[i].children[0].classes['link']).toBe(true);
      expect(root.children[0].children[1].children[2].children[1].children[i].children[0].attributes['href']).toBe('https://host' + app.links[i].link);
      expect(root.children[0].children[1].children[2].children[1].children[i].children[0].attributes['target']).toBe('_blank');
    }
  }));

  it('View: Should set alert on isServerDown emits', fakeAsync(() => {
    PingService.isServerDown.set(true);

    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;

    tick(1100);

    fixture.detectChanges();

    const root = fixture.debugElement.query(By.css('div'));

    expect(app.isServerDown()).toBe(true);

    expect(root.children.length).toBe(4);
    expect(root.children[3].classes['toast']).toBe(true);
  }));

  it('View: Should hide alert on isServerDown emits', fakeAsync(() => {
    PingService.isServerDown.set(false);
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;

    tick(1100);

    fixture.detectChanges();

    const root = fixture.debugElement.query(By.css('div'));

    expect(app.isServerDown()).toBe(false);

    expect(root.children.length).toBe(3);
  }));
});
