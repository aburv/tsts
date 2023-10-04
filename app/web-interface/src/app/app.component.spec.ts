import { TestBed, fakeAsync, tick } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { AppComponent } from './app.component';
import { Router } from '@angular/router';
import { ThemeService } from './_services/theme.service';
import { UserService } from './_services/user.service';
import { of, throwError } from 'rxjs';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { By } from '@angular/platform-browser';

describe('AppComponent', () => {
  const userService = jasmine.createSpyObj('UserService', [
    'loadUserData'
  ]);
  userService.loadUserData.and.returnValue(of(''));

  const themeService = jasmine.createSpyObj('ThemeService', [
    'getOptions',
    'setTheme',
  ]);
  themeService.getOptions.and.returnValue(['light', 'dark']);
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
      }
    ],
    declarations: [AppComponent],
    schemas: [CUSTOM_ELEMENTS_SCHEMA]
  }));

  beforeEach(() => {
    userService.loadUserData.calls.reset();
    themeService.getOptions.calls.reset();
    themeService.setTheme.calls.reset();
  })

  it('Should create the app on success loading data', fakeAsync(() => {
    const initThemeSpy = spyOn(AppComponent.prototype, 'initTheme');
    class Media implements MediaQueryList {
      matches: boolean = true;
      media: string = '';
      onchange: ((this: MediaQueryList, ev: MediaQueryListEvent) => any) | null = null;
      addListener(callback: ((this: MediaQueryList, ev: MediaQueryListEvent) => any) | null): void { }
      removeListener(callback: ((this: MediaQueryList, ev: MediaQueryListEvent) => any) | null): void { }
      addEventListener<K extends 'change'>(type: K, listener: (this: MediaQueryList, ev: MediaQueryListEventMap[K]) => any, options?: boolean | AddEventListenerOptions | undefined): void;
      addEventListener(type: string, listener: EventListenerOrEventListenerObject, options?: boolean | AddEventListenerOptions | undefined): void;
      addEventListener(type: unknown, listener: unknown, options?: unknown): void { }
      removeEventListener<K extends 'change'>(type: K, listener: (this: MediaQueryList, ev: MediaQueryListEventMap[K]) => any, options?: boolean | EventListenerOptions | undefined): void;
      removeEventListener(type: string, listener: EventListenerOrEventListenerObject, options?: boolean | EventListenerOptions | undefined): void;
      removeEventListener(type: unknown, listener: unknown, options?: unknown): void { }
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
    expect(themeService.getOptions).toHaveBeenCalledOnceWith();
    expect(userService.loadUserData).toHaveBeenCalledOnceWith();
    expect(app.initTheme).toHaveBeenCalledOnceWith(true);
    expect(window.matchMedia).toHaveBeenCalledOnceWith("(prefers-color-scheme: dark)");

    initThemeSpy.calls.reset();

    tick(1100);

    expect(app.isInInit).toBe(false);

    expect(media.addEventListener).toHaveBeenCalledWith('change', jasmine.any(Function))

    // expect(app.initTheme).toHaveBeenCalledOnceWith(true);
  }));

  it('Should create the app on failure loading data', fakeAsync(() => {
    const initThemeSpy = spyOn(AppComponent.prototype, 'initTheme');
    userService.loadUserData.and.returnValue(throwError(''));

    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;

    expect(app).toBeTruthy();

    expect(app.isInInit).toBe(true);
    expect(themeService.getOptions).toHaveBeenCalledOnceWith();
    expect(userService.loadUserData).toHaveBeenCalledOnceWith();

    initThemeSpy.calls.reset();

    tick(1100);

    expect(app.isInInit).toBe(false);

    userService.loadUserData.calls.reset();
  }));

  it('Should set dark theme on initTheme ', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;

    const selectThemeSpy = spyOn(app, 'selectTheme');

    app.initTheme(true);

    expect(app.selectTheme).toHaveBeenCalledOnceWith('dark');
    selectThemeSpy.calls.reset();
  });

  it('Should set light theme on initTheme ', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;

    const selectThemeSpy = spyOn(app, 'selectTheme');

    app.initTheme(false);

    expect(app.selectTheme).toHaveBeenCalledOnceWith('light');
    selectThemeSpy.calls.reset();
  });

  it('Should set theme on selected theme', () => {
    const initThemeSpy = spyOn(AppComponent.prototype, 'initTheme');

    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;

    app.selectTheme('dark');

    expect(themeService.setTheme).toHaveBeenCalledOnceWith('dark');
    expect(app.themeSelected).toBe('dark')
    initThemeSpy.calls.reset();
  });

  it('Should set search text on onChange call', () => {
    const initThemeSpy = spyOn(AppComponent.prototype, 'initTheme');

    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;

    app.onChange({ target: { value: 'value' } });

    expect(app.searchText()).toBe('value')
    initThemeSpy.calls.reset();
  });

  it('Should navigate to dashboard', () => {
    const initThemeSpy = spyOn(AppComponent.prototype, 'initTheme');

    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;

    app.navigateToDashboard();

    expect(router.navigate).toHaveBeenCalledOnceWith(['home']);
    initThemeSpy.calls.reset();
  });

  it('View: Should set root with screen and layout classes and its children', fakeAsync(() => {
    const initThemeSpy = spyOn(AppComponent.prototype, 'initTheme');

    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;

    fixture.detectChanges();

    const root = fixture.debugElement.query(By.css('div'));

    expect(root.classes['screen']).toBe(true);
    expect(root.classes['layout']).toBe(true);

    expect(root.children.length).toBe(3);
    expect(root.children[0].classes['splashLayout']).toBe(true);
    expect(root.children[1].classes['app-support-layout']).toBe(true);
    expect(root.children[2].classes['footer-layout']).toBe(true);

    expect(root.children[0].children.length).toBe(1);
    expect(root.children[0].children[0].children.length).toBe(2);
    const img = root.children[0].children[0].query(By.css('img'));

    expect(root.children[0].children[0].children[0]).toEqual(img);
    expect(root.children[0].children[0].children[0].classes['loader']).toBe(true);
    expect(img.attributes['src']).toBe('../assets/logo_app.png');
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
    expect(root.children[2].children[0].nativeElement.textContent).toBe('Powered by Aburv | Takbuff © 2023 An open source application');

    initThemeSpy.calls.reset();
  }));

  it('View: Should set content and its children', fakeAsync(() => {
    const initThemeSpy = spyOn(AppComponent.prototype, 'initTheme');

    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;

    spyOn(app, 'navigateToDashboard')
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
    expect(img.attributes['src']).toBe('../assets/logo_app.png');
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
    expect(root.children[0].children[1].children[2].classes['side-bar-layout']).toBe(true);

    icon[0].triggerEventHandler('click');
    app.searchText.set('value')
    const result = ['']
    app.searchResult = result;

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
    expect(app.searchText()).toBe('');
    icon[1].triggerEventHandler('click');
    expect(app.isSearching).toBe(false);

    expect(root.children[0].children[0].children[2].children[1].classes['disp-input']).toBe(true);

    input.triggerEventHandler('keyup', { target: { value: '' } });
    expect(app.onChange).toHaveBeenCalledOnceWith({ target: { value: '' } });

    expect(root.children[0].children[1].children[1].classes['main-layout']).toBe(true);
    expect(root.children[0].children[1].children[1].children.length).toBe(result.length);
    for (let i = 0; i < result.length; i++) {
      expect(root.children[0].children[1].children[1].children[i].classes['search-result-item']).toBe(true);
    }

    initThemeSpy.calls.reset();
  }));

  it('View: Should set loading layout', fakeAsync(() => {
    const initThemeSpy = spyOn(AppComponent.prototype, 'initTheme');

    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;

    tick(1100);

    app.isLoading = true;

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
    expect(img.attributes['src']).toBe('../assets/logo_app.png');


    initThemeSpy.calls.reset();
  }));

});
