import { Component, computed, ElementRef, Signal, signal, ViewChild, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterOutlet } from '@angular/router';
import { toObservable } from '@angular/core/rxjs-interop';
import { debounceTime, distinctUntilChanged, switchMap } from 'rxjs/operators';
import { Observable, Observer, fromEvent, merge, of } from 'rxjs';
import { map } from 'rxjs/operators';

import { ThemeService } from './_services/theme.service';
import { UserService } from './_services/user.service';
import { LoaderService } from './_services/loader.service';
import { PingService } from './_services/ping.service';
import { DeviceService } from './_services/device.service';
import { SearchService } from './_services/search.service';
import { Config } from './config';

import { Icon, IconComponent } from './components/icon/icon.component';

import { UserButtonComponent } from './components/user-button/user-button.component';
import { ImageComponent } from './components/image/image.component';

@Component({
  selector: 'app-root',
  imports: [
    RouterOutlet,
    CommonModule,
    IconComponent,
    ImageComponent,
    UserButtonComponent,
  ],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  private router = inject(Router);
  private themeService = inject(ThemeService);
  private loaderService = inject(LoaderService);
  private userService = inject(UserService);
  private deviceService = inject(DeviceService);
  private searchService = inject(SearchService);
  private pingService = inject(PingService);

  @ViewChild('searchInput') searchInput!: ElementRef;

  readonly Icon = Icon
  isInInit = true;
  isLoading = computed(() => {
    return LoaderService.status();
  });
  isServerDown: Signal<boolean> = computed(() => {
    return PingService.isServerDown();
  });

  isInternetDown = signal(false);

  isSearching  = signal<boolean>(false);

  searchText = signal<string>('');

  searchResult = signal<{ [key: string]: any[] } | null>(null);

  thisyear = new Date().getFullYear();

  siteDomain = Config.getSiteDomain();

  links = [
    {
      title: 'Terms & Conditions',
      link: '/terms'
    },
    {
      title: 'Help',
      link: '/support'
    },
    {
      title: 'Blog',
      link: '/blogs'
    },
    {
      title: 'Privacy Policies',
      link: '/privacy'
    },
    {
      title: 'FAQ',
      link: '/faq'
    },
    {
      title: 'Newsletters',
      link: '/newsletters'
    },
    {
      title: 'About Sepak Takraw Game',
      link: '/about-game'
    },
  ]

  objectKeys = Object.keys;

  constructor() {
    const userService = this.userService;
    const deviceService = this.deviceService;

    const isThemeDark = window.matchMedia("(prefers-color-scheme: dark)");
    this.themeService.initTheme(isThemeDark.matches);
    isThemeDark.addEventListener("change", (e: MediaQueryListEvent) => {
      this.themeService.initTheme(e.matches);
    });

    merge(
      fromEvent(window, 'offline').pipe(map(() => false)),
      fromEvent(window, 'online').pipe(map(() => true)),
      new Observable((sub: Observer<boolean>) => {
        sub.next(navigator.onLine);
        sub.complete();
      })
    ).subscribe((isOnline: boolean) => {
      this.isInternetDown.set(!isOnline)
    });

    deviceService.sendDeviceDetails()

    userService.getUserData().subscribe({
      next: () => {
        setTimeout(() => {
          this.isInInit = false;
        }, 1000);
      },
      error: () => {
        setTimeout(() => {
          this.isInInit = false;
        }, 500);
      }
    });

    toObservable(this.searchText).pipe(
      debounceTime(1500),
      distinctUntilChanged(),
      switchMap(query => {
        if (!query.trim()) return of({});
        return this.searchService.get(this.searchText());
      })
    ).subscribe((data: any) => {
      this.searchResult.set(data["data"])
    });
  }

  turnToSearching(): void {
    if (!this.isSearching()) {
      this.isSearching.set(true);
      setTimeout(() => {
        this.searchInput.nativeElement.focus();
      }, 500)
    }
  }

  onChange(event: any): void {
    this.searchText.set(event.target.value);
  }

  onSearchClose(): void {
    this.searchText.set('');
    this.isSearching.set(false);
  }

  navigateToDashboard(): void {
    this.router.navigate(['home']);
  }

  navigate(domain: string, id: string): void {
    this.router.navigate([domain, id]);
  }
}
