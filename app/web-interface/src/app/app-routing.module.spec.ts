import { Location } from '@angular/common';
import { TestBed, fakeAsync, tick } from '@angular/core/testing';
import { Router } from '@angular/router';
import { RouterTestingModule } from '@angular/router/testing';
import { routes } from './app-routing.module';
import { AppModule } from './app.module';

describe('The App Routing', () => {
  let router: Router;
  let location: Location;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [AppModule, RouterTestingModule.withRoutes(routes)]
    });

    router = TestBed.get(Router) as Router;
    location = TestBed.get(Location) as Location;
  });

  it('Should automatically redirects to home when the app starts',
    fakeAsync(() => {
      router.navigate(['']);
      tick();
      expect(location.path()).toBe('/home');
    })
  );

  it('Should directs to  when invoking /0',
    fakeAsync(() => {
      router.navigate(['/home']);
      tick();
      expect(location.path()).toBe('/home');
    })
  );
});