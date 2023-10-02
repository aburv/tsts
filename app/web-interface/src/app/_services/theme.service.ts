import {Injectable} from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class ThemeService {

  getOptions(): Array<string>{
    return ['Light', 'Dark']
  }

  setTheme(name: string) {
    document.documentElement.setAttribute('theme', name.toLowerCase());
  }
}