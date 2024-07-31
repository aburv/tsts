import { Component, ElementRef, signal, ViewChild } from '@angular/core';
import { ThemeService } from './_services/theme.service';
import { UserService } from './_services/user.service';
import { Router } from '@angular/router';
import { LoaderService } from './_services/loader.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  @ViewChild('searchInput') searchInput!: ElementRef;

  isInInit = true;
  isLoading = false;

  isSearching = false;

  searchText = signal<string>('');

  toggleSearch(): void {
    if (!this.isSearching) {
      this.isSearching = true;
      setTimeout(() => {
        this.searchInput.nativeElement.focus();
      }, 500)
    }
  }

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
    private userService: UserService
  ) {
    const isThemeDark = window.matchMedia("(prefers-color-scheme: dark)");
    this.themeService.initTheme(isThemeDark.matches);
    isThemeDark.addEventListener("change", (e: MediaQueryListEvent) => {
      this.themeService.initTheme(e.matches);
    });

    userService.loadUserData().subscribe(() => {
      setTimeout(() => {
        this.isInInit = false;
      }, 1000);
    }, () => {
      setTimeout(() => {
        this.isInInit = false;
      }, 500);
    })

    loaderService.getIsLoading().subscribe((status: boolean) => {
      this.isLoading = status;
    });
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
