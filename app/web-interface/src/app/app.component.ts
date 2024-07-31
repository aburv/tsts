import { Component, computed, ElementRef, Signal, signal, ViewChild } from '@angular/core';
import { ThemeService } from './_services/theme.service';
import { UserService } from './_services/user.service';
import { Router } from '@angular/router';
import { LoaderService } from './_services/loader.service';
import { PingService } from './_services/ping.service';

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

  isSearching = false;

  searchText = signal<string>('');

  searchResult: Array<string> = []

  thisyear = new Date().getFullYear();

  links = [
    {
      title: 'Terms & Conditions',
      link: ''
    },
    {
      title: 'Help',
      link: ''
    },
    {
      title: 'Blog',
      link: ''
    },
    {
      title: 'Privacy Policies',
      link: ''
    },
    {
      title: 'FAQ',
      link: ''
    },
    {
      title: 'Newsletters',
      link: ''
    },
    {
      title: 'About Sepak Takraw Game',
      link: ''
    },
  ]

  constructor(
    private router: Router,
    private themeService: ThemeService,
    private loaderService: LoaderService,
    private userService: UserService,
    private pingService: PingService
  ) {
    const isThemeDark = window.matchMedia("(prefers-color-scheme: dark)");
    this.themeService.initTheme(isThemeDark.matches);
    isThemeDark.addEventListener("change", (e: MediaQueryListEvent) => {
      this.themeService.initTheme(e.matches);
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
  }

  onSearchClose(): void {
    this.searchText.set('');
    this.isSearching = false;
  }

  navigateToDashboard(): void {
    this.router.navigate(['home']);
  }
}
