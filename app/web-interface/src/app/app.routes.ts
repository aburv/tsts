import { Routes } from '@angular/router';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { PlayerComponent } from './pages/player/player.component';

export const routes: Routes = [
  {
    path: 'home', 
    component: DashboardComponent,
    title: 'Home | Takbuff',
  },
  {
    path: 'player/:id',
    component: PlayerComponent,
    title: 'Player | Takbuff',
  },
  { path: '**', redirectTo: 'home' },
];
