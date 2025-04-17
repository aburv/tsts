import { NgModule } from '@angular/core';
import { Routes, RouterModule, Router } from '@angular/router';

import { DashboardComponent } from './pages/dashboard/dashboard.component';

export const routes: Routes = [
  {
    path: 'home', component: DashboardComponent,
  },
  { path: '**', redirectTo: 'home' },
];


@NgModule({
  imports: [RouterModule.forRoot(routes, {
    onSameUrlNavigation: 'reload'
  })],
  exports: [RouterModule]
})
export class AppRoutingModule {
  public constructor(private router: Router) { }
}
