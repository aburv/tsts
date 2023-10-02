import { ThemeService } from "./theme.service";

describe('ThemeServices', () => {
  it('Should set theme attribute on setTheme call', () => {
    spyOn(document.documentElement, 'setAttribute');
    
    new ThemeService().setTheme('Theme');

    expect(document.documentElement.setAttribute).toHaveBeenCalledOnceWith('theme', 'theme');
  });

  it('Should set theme attribute on setTheme call', () => {    
    const options = new ThemeService().getOptions();

    expect(options).toEqual(['Light', 'Dark']);
  });
});
