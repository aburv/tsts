import { Component, computed, DestroyRef, ElementRef, inject, Signal, signal, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterOutlet } from '@angular/router';
import { toObservable } from '@angular/core/rxjs-interop';
import { debounceTime, distinctUntilChanged, switchMap } from 'rxjs/operators';
import { Observable, Observer, fromEvent, merge, of } from 'rxjs';
import { map } from 'rxjs/operators';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

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

  private initTimeout?: ReturnType<typeof setTimeout>;
  private searchTimeout?: ReturnType<typeof setTimeout>;
  private readonly destroyRef = inject(DestroyRef);

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

  searchResult = signal<Record<string, any[]> | null>(null);

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

    this.destroyRef.onDestroy(() => {
      if (this.initTimeout) {
        clearTimeout(this.initTimeout);
      }
      if (this.searchTimeout) {
        clearTimeout(this.searchTimeout);
      }
    });

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
    ).pipe(takeUntilDestroyed(this.destroyRef)).subscribe((isOnline: boolean) => {
      this.isInternetDown.set(!isOnline)
    });

    deviceService.sendDeviceDetails()

    userService.getUserData().pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: () => {
        this.initTimeout = setTimeout(() => {
          this.isInInit = false;
        }, 1000);
      },
      error: () => {
        this.initTimeout = setTimeout(() => {
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
      this.searchTimeout = setTimeout(() => {
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
