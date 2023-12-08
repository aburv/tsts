import { Component, computed, signal } from '@angular/core';
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

  isInInit = true;
  isLoading = false;

  isSearching = false;

  searchText = signal<string>('');

  searchResult: Array<String> = []

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

    loaderService.getIsLoading().subscribe((status)=>{
      this.isLoading = status;
    })
  }

  onChange(event: any): void {
    this.searchText.set(event.target.value);
  }

  navigateToDashboard(): void {
    this.router.navigate(['home']);
    }
}
