import { NgModule } from '@angular/core';
import { Routes, RouterModule, Router } from '@angular/router';

import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { PlayerComponent } from './pages/player/player.component';

export const routes: Routes = [
  {
    path: 'home', component: DashboardComponent,
  },
  {
    path: 'player/:id', component: PlayerComponent,
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
