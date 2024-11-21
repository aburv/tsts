import { ThemeService } from "./theme.service";

describe('ThemeServices', () => {
  it('Should set theme attribute on setTheme call', () => {
    spyOn(document.documentElement, 'setAttribute');
    
    new ThemeService().setTheme('Theme');

    expect(document.documentElement.setAttribute).toHaveBeenCalledOnceWith('theme', 'theme');
  });

  it('Should set dark theme on initTheme ', () => {
    const service = new ThemeService();

    const setThemeSpy = spyOn(service, 'setTheme');

    service.initTheme(true);

    expect(service.setTheme).toHaveBeenCalledOnceWith('Dark');
    setThemeSpy.calls.reset();
  });

  it('Should set light theme on initTheme ', () => {
    const service = new ThemeService();

    const setThemeSpy = spyOn(service, 'setTheme');

    service.initTheme(false);

    expect(service.setTheme).toHaveBeenCalledOnceWith('Light');
    setThemeSpy.calls.reset();
  });
});
