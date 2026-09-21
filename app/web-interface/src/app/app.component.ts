import { Component, computed, DestroyRef, ElementRef, inject, Signal, signal, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterOutlet } from '@angular/router';
import { Observable, Observer, fromEvent, merge } from 'rxjs';
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

@Component({
  selector: 'app-root',
  imports: [
    RouterOutlet, 
    CommonModule,
    IconComponent,
    UserButtonComponent,
  ],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
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

  isSearching = false;

  searchText = signal<string>('');

  searchResult: Array<string> = []

  thisyear = new Date().getFullYear();

  siteDomain = Config.getSiteDomain();

  links = [
    {
      title: 'Terms & Conditions',
      link: '/terms'
    },
    {
      title: 'Help',
      link: '/faq'
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

  constructor(
    private router: Router,
    private themeService: ThemeService,
    private loaderService: LoaderService,
    private userService: UserService,
    private deviceService: DeviceService,
    private searchService: SearchService,
    private pingService: PingService
  ) {
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
  }

  turnToSearching(): void {
    if (!this.isSearching) {
      this.isSearching = true;
      this.searchTimeout = setTimeout(() => {
        this.searchInput.nativeElement.focus();
      }, 500)
    }
  }

  onChange(event: any): void {
    this.searchText.set(event.target.value);
    if (this.searchText() !== "") {
      this.searchService.get(this.searchText()).subscribe((data: any) => {
        this.searchResult = data["data"]
      });
    }
  }

  onSearchClose(): void {
    this.searchText.set('');
    this.isSearching = false;
  }

  navigateToDashboard(): void {
    this.router.navigate(['home']);
  }
}
