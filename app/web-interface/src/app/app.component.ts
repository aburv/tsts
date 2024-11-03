import { Component, computed, ElementRef, Signal, signal, ViewChild } from '@angular/core';
import { Observable, Observer, fromEvent, merge } from 'rxjs';
import { map } from 'rxjs/operators';

import { ThemeService } from './_services/theme.service';
import { UserService } from './_services/user.service';
import { Router } from '@angular/router';
import { LoaderService } from './_services/loader.service';
import { PingService } from './_services/ping.service';
import { SearchService } from './_services/search.service';
import { Config } from './config';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  @ViewChild('searchInput') searchInput!: ElementRef;

  isInInit = true;
  isLoading = false;
  isServerDown: Signal<boolean> = computed(() => {
    return this.pingService.getIsServerDown()();
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
      link: '/terms-conditions'
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
      link: '/privacy-policies'
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
    private searchService: SearchService,
    private pingService: PingService
  ) {
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

    loaderService.getIsLoading().subscribe((status: boolean) => {
      this.isLoading = status;
    });
  }

  turnToSearching(): void {
    if (!this.isSearching) {
      this.isSearching = true;
      setTimeout(() => {
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
