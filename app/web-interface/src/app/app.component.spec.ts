import { TestBed, fakeAsync, flush, tick } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { AppComponent } from './app.component';
import { Router } from '@angular/router';
import { ThemeService } from './_services/theme.service';
import { UserService } from './_services/user.service';
import { of, throwError } from 'rxjs';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { HttpClientTestingModule } from '@angular/common/http/testing';
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

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RouterTestingModule, AppComponent, HttpClientTestingModule],
      providers: [
        { provide: Router, useValue: router },
        { provide: ThemeService, useValue: themeService },
        { provide: UserService, useValue: userService },
        { provide: DeviceService, useValue: deviceService },
        { provide: SearchService, useValue: searchService },
        { provide: LoaderService, useValue: loaderService },
        { provide: PingService, useValue: pingService },
      ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA]
    }).compileComponents();

    const googleSpy = {
      initialize: jasmine.createSpy('initialize'),
      renderButton: jasmine.createSpy('renderButton'),
      prompt: jasmine.createSpy('prompt'),
    };
    (window as any).google = { accounts: { id: googleSpy } };

    userService.getUserData.calls.reset();
    deviceService.sendDeviceDetails.calls.reset();
    themeService.initTheme.calls.reset();
    themeService.setTheme.calls.reset();
    searchService.get.calls.reset();
    router.navigate.calls.reset();
    
    LoaderService.status.set(false);
    PingService.isServerDown.set(false);

    spyOn(Config, "getSiteDomain").and.returnValue("https://host");
  });

  let fixture: any;
  let app: any;
  let media: any;

  beforeEach(() => {
    media = {
      matches: true,
      media: '',
      onchange: null,
      addListener: jasmine.createSpy('addListener'),
      removeListener: jasmine.createSpy('removeListener'),
      addEventListener: jasmine.createSpy('addEventListener'),
      removeEventListener: jasmine.createSpy('removeEventListener'),
      dispatchEvent: jasmine.createSpy('dispatchEvent').and.returnValue(false),
    };

    spyOn(window, 'matchMedia').and.returnValue(media);
  });

  it('Should create the app on success loading data', fakeAsync(() => {

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

  it('Should respond to loading state changes', fakeAsync(() => {
    fixture = TestBed.createComponent(AppComponent);
    app = fixture.componentInstance;

    LoaderService.status.set(true);
    tick();
    fixture.detectChanges();
    expect(app.isLoading()).toBe(true);

    LoaderService.status.set(false);
    tick();
    fixture.detectChanges();
    expect(app.isLoading()).toBe(false);
  }));

  it('Should handle user data loading failure gracefully', fakeAsync(() => {
    userService.getUserData.and.returnValue(throwError(() => new Error('Failed to load')));

    fixture = TestBed.createComponent(AppComponent);
    app = fixture.componentInstance;

    expect(app).toBeTruthy();
    expect(app.isInInit).toBe(true);
    expect(userService.getUserData).toHaveBeenCalledTimes(1);

    tick(1100);
    fixture.detectChanges();

    expect(app.isInInit).toBe(false);
  }));

  it('Should handle search text changes correctly', fakeAsync(() => {
    fixture = TestBed.createComponent(AppComponent);
    app = fixture.componentInstance;

    app.onChange({ target: { value: 'search-term' } });
    tick();
    expect(app.searchText()).toBe('search-term');
    expect(searchService.get).toHaveBeenCalledOnceWith('search-term');

    searchService.get.calls.reset();
    app.onChange({ target: { value: '' } });
    tick();
    expect(app.searchText()).toBe('');
    expect(searchService.get).not.toHaveBeenCalled();
  }));

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

    expect(root.children[0].classes['splash-layout']).toBe(true);
    expect(root.children[1].classes['app-support-layout']).toBe(true);
    expect(root.children[2].classes['footer-layout']).toBe(true);

    const splashInner = root.children[0].children[0];
    const img = splashInner.query(By.css('img'));
    const text = splashInner.children[1];

    expect(img.classes['loader']).toBe(true);
    expect(img.attributes['src']).toBe('../assets/logo_app_164.png');
    expect(text.nativeElement.textContent).toBe('Takbuff');
    expect(text.styles['text-align']).toBe('center');
    expect(text.styles['font-size']).toBe('30px');

    tick(1100);
    fixture.detectChanges();

    expect(root.children.length).toBe(3);
    expect(root.children[0].classes['content']).toBe(true);
    expect(root.children[1].classes['app-support-layout']).toBe(true);
    expect(root.children[2].classes['footer-layout']).toBe(true);

    const appSupportIcons = root.children[1].queryAll(By.css('app-icon'));
    const breakLine = root.children[1].query(By.css('br'));
    expect(appSupportIcons.length).toBe(2);
    expect(appSupportIcons[0].componentInstance.name()).toBe('android');
    expect(appSupportIcons[0].componentInstance.size()).toBe(30);
    expect(appSupportIcons[1].componentInstance.name()).toBe('ios');
    expect(appSupportIcons[1].componentInstance.size()).toBe(30);

    const footer = root.children[2].children[0];
    expect(footer.classes['footer']).toBe(true);
    
    const footerLinks = footer.children[0];
    expect(footerLinks.classes['links']).toBe(true);
    expect(footerLinks.classes['bottom']).toBe(true);
    expect(footerLinks.children.length).toBe(2 * app.links.length - 1);

    const links = footerLinks.queryAll(By.css('a'));
    expect(links.length).toBe(app.links.length);
    links.forEach((link, i) => {
      expect(link.nativeElement.textContent.trim()).toBe(app.links[i].title);
      expect(link.classes['link']).toBe(true);
      expect(link.attributes['href']).toBe('https://host' + app.links[i].link);
      expect(link.attributes['target']).toBe('_blank');
    });

    const footerText = footer.children[1];
    const footerSpans = footerText.queryAll(By.css('span'));
    expect(footerSpans[0].nativeElement.textContent).toContain('Powered by Aburv | Takbuff ©');
    expect(footerText.query(By.css('.break'))).toBeTruthy();
    expect(footerSpans[1].nativeElement.textContent.trim()).toBe('An Open Source Application');
    expect(footerSpans[1].styles['font-size']).toBe('12px');

    const sideBarLinks = root.children[0].children[1].children[2].children[1];
    expect(sideBarLinks.classes['links']).toBe(true);
    expect(sideBarLinks.classes['side']).toBe(true);
    
    const sideLinks = sideBarLinks.queryAll(By.css('a'));
    expect(sideLinks.length).toBe(app.links.length);
    sideLinks.forEach((link, i) => {
      expect(link.nativeElement.textContent.trim()).toBe(app.links[i].title);
      expect(link.classes['link']).toBe(true);
      expect(link.attributes['href']).toBe('https://host' + app.links[i].link);
      expect(link.attributes['target']).toBe('_blank');
    });

    const separators = sideBarLinks.queryAll(By.css('.separator'));
    expect(separators.length).toBe(4);
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
    const content = root.children[0];

    expect(root.children.length).toBe(3);
    expect(content.classes['content']).toBe(true);
    
    const header = content.children[0];
    expect(header.classes['header-layout']).toBe(true);
    
    const title = header.children[0];
    expect(title.classes['title']).toBe(true);
    title.triggerEventHandler('click');
    expect(app.navigateToDashboard).toHaveBeenCalledOnceWith();
    
    const titleImg = title.query(By.css('img'));
    const titleText = title.query(By.css('b'));
    expect(titleImg.attributes['src']).toBe('../assets/logo_app_164.png');
    expect(titleText.nativeElement.textContent).toBe('Takbuff');
    expect(titleText.styles['color']).toBe('rgb(238, 238, 238)');

    expect(header.children[1].classes['spacer']).toBe(true);

    const search = header.children[2];
    expect(search.classes['search']).toBe(true);
    
    const searchIcon = search.query(By.css('app-icon'));
    const searchInput = search.query(By.css('input'));
    
    expect(searchIcon.componentInstance.name()).toBe('search');
    expect(searchIcon.componentInstance.size()).toBe(30);
    expect(searchIcon.styles['cursor']).toBe('pointer');
    
    expect(searchInput.attributes['placeholder']).toBe('Search here');
    expect(searchInput.nativeElement.value).toBe('');

    const userButton = header.query(By.css('app-user-button'));
    expect(userButton).toBeTruthy();

    const layout = content.children[1];
    expect(layout.classes['layout']).toBe(true);
    expect(layout.children.length).toBe(3);

    expect(layout.children[0].classes['side-bar-layout']).toBe(true);
    
    const mainContent = layout.children[1];
    expect(mainContent.classes['main-layout']).toBe(true);
    expect(mainContent.query(By.css('router-outlet'))).toBeTruthy();

    const rightSide = layout.children[2];
    expect(rightSide.children[0].classes['side-bar-layout']).toBe(true);

    searchIcon.triggerEventHandler('click');
    expect(app.turnToSearching).toHaveBeenCalledOnceWith();
    
    app.searchText.set('value')
    const result = ['']
    app.searchResult = result;
    app.isSearching = true;

    fixture.detectChanges();

    const searchIconsAfter = search.queryAll(By.css('app-icon'));
    expect(searchIconsAfter.length).toBe(2);
    expect(searchIconsAfter[0].styles['cursor']).toBe('default');
    expect(searchIconsAfter[1].componentInstance.name()).toBe('cross');
    expect(searchIconsAfter[1].componentInstance.size()).toBe(20);
    expect(searchIconsAfter[1].styles['cursor']).toBe('pointer');

    const searchMainContent = layout.query(By.css('.main-layout'));
    const searchResults = searchMainContent.queryAll(By.css('.search-result-item'));
    expect(searchResults.length).toBe(result.length);
    
    expect(app.searchText()).toBe('value');
    searchIconsAfter[1].triggerEventHandler('click');
    expect(app.onSearchClose).toHaveBeenCalledOnceWith();

    expect(searchInput.classes['disp-input']).toBe(true);

    searchInput.triggerEventHandler('keyup', { target: { value: '' } });
    expect(app.onChange).toHaveBeenCalledOnceWith({ target: { value: '' } });
    
    flush();
  }));

  it('View: Should show loading layout when loading', fakeAsync(() => {
    const fixture = TestBed.createComponent(AppComponent);

    tick(1100);
    LoaderService.status.set(true);
    fixture.detectChanges();

    const root = fixture.debugElement.query(By.css('div'));

    expect(root.children.length).toBe(4);
    expect(root.children[0].classes['content']).toBe(true);
    expect(root.children[1].classes['app-support-layout']).toBe(true);
    expect(root.children[2].classes['footer-layout']).toBe(true);
    expect(root.children[3].classes['loader-layout']).toBe(true);

    const loaderLayout = root.children[3];
    const loaderImg = loaderLayout.query(By.css('img'));
    expect(loaderImg.classes['loader']).toBe(true);
    expect(loaderImg.attributes['src']).toBe('../assets/logo_app_164.png');
  }));

  it('View: Should show links in the right sidebar', fakeAsync(() => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;

    tick(1100);
    fixture.detectChanges();

    const root = fixture.debugElement.query(By.css('div'));
    const content = root.children[0];
    const layout = content.children[1];
    const rightSide = layout.children[2];
    const sidebarLinks = rightSide.children[1];

    expect(sidebarLinks.classes['links']).toBe(true);
    expect(sidebarLinks.classes['side']).toBe(true);

    const links = sidebarLinks.queryAll(By.css('a'));
    expect(links.length).toBe(app.links.length);
    
    links.forEach((link, i) => {
      expect(link.nativeElement.textContent.trim()).toBe(app.links[i].title);
      expect(link.classes['link']).toBe(true);
      expect(link.attributes['href']).toBe('https://host' + app.links[i].link);
      expect(link.attributes['target']).toBe('_blank');
    });

    const separators = sidebarLinks.queryAll(By.css('.separator'));
    expect(separators.length).toBe(4);

    const separatorIndices = [0, 1, 3, 4];
    separatorIndices.forEach(index => {
      const link = links[index];
      const nextElement = link.nativeElement.nextElementSibling;
      expect(nextElement.textContent).toBe('|');
    });
  }));

  it('View: Should show server down alert', fakeAsync(() => {
    PingService.isServerDown.set(true);
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;

    tick(1100);
    fixture.detectChanges();

    expect(app.isServerDown()).toBe(true);

    const root = fixture.debugElement.query(By.css('div'));
    const toast = root.query(By.css('.toast'));
    expect(toast).toBeTruthy();
    expect(toast.nativeElement.textContent.trim()).toBe('Please try again later');
  }));

  it('View: Should show internet down alert', fakeAsync(() => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;

    tick(1100);
    app.isInternetDown.set(true);
    fixture.detectChanges();

    const root = fixture.debugElement.query(By.css('div'));
    const toast = root.query(By.css('.toast'));
    expect(toast).toBeTruthy();
    expect(toast.nativeElement.textContent.trim()).toBe('No Internet connection');
  }));

  it('View: Should hide alerts when services are up', fakeAsync(() => {
    PingService.isServerDown.set(false);
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;

    tick(1100);
    app.isInternetDown.set(false);
    fixture.detectChanges();

    const root = fixture.debugElement.query(By.css('div'));
    const toast = root.query(By.css('.toast'));
    expect(toast).toBeFalsy();
  }));
});
