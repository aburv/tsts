import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { Router } from '@angular/router';
import { Location } from '@angular/common';

import { routes } from './app.routes';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { PlayerComponent } from './pages/player/player.component';

describe('App Routes', () => {
  let router: Router;
  let location: Location;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      providers: [
        provideRouter(routes),
      ]
    }).compileComponents();

    router = TestBed.inject(Router);
    location = TestBed.inject(Location);
  });

  function getActiveRoute() {
    return router.routerState.snapshot.root.firstChild!;
  }

  it('Should load DashboardComponent for /home', async () => {
    await router.navigateByUrl('/home');

    const route = getActiveRoute();

    expect(location.path()).toBe('/home');
    expect(route.routeConfig?.component).toBe(DashboardComponent);
  });

  it('Should load PlayerComponent for /player/:id', async () => {
    await router.navigateByUrl('/player/7');

    const route = getActiveRoute();

    expect(location.path()).toBe('/player/7');
    expect(route.routeConfig?.component).toBe(PlayerComponent);
  });

  it('Should redirect unknown path to /home', async () => {
    await router.navigateByUrl('/unknown/path');

    const route = getActiveRoute();

    expect(location.path()).toBe('/home');
    expect(route.routeConfig?.component).toBe(DashboardComponent);
  });
});
