import { Component, computed, signal } from '@angular/core';
import { ThemeService } from './_services/theme.service';
import { UserService } from './_services/user.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  isInInit = true;
  isLoading = false;

  isSearching = false;

  themeOptions: Array<string> = [];
  themeSelected!: string;

  searchText = signal<string>('');

  searchResult: Array<String> = []

  constructor(
    private router: Router,
    private themeService: ThemeService,
    private userService: UserService
  ) {
    this.themeOptions = this.themeService.getOptions();
    const isThemeDark = window.matchMedia("(prefers-color-scheme: dark)");
    this.initTheme(isThemeDark.matches);
    // this.initTheme(isThemeDark.matches);
    isThemeDark.addEventListener("change", (e: MediaQueryListEvent) => {
      this.initTheme(e.matches);
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
  }

  initTheme(isDark: boolean): void {
    if (isDark) {
      this.selectTheme(this.themeOptions[1]);
    } else {
      this.selectTheme(this.themeOptions[0]);
    }
  }

  selectTheme(theme: string): void {
    this.themeSelected = theme;
    this.themeService.setTheme(this.themeSelected);
  }

  onChange(event: any): void {
    this.searchText.set(event.target.value);
  }

  navigateToDashboard(): void {
    this.router.navigate(['home']);
  }
}
