import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class ThemeService {
  private options = ['Light', 'Dark']

  initTheme(isDark: boolean): void {
    if (isDark) {
      this.setTheme(this.options[1]);
    } else {
      this.setTheme(this.options[0]);
    }
  }

  setTheme(name: string): void {
    document.documentElement.setAttribute('theme', name.toLowerCase());
  }
}