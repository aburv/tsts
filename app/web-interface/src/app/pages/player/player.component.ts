import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { LoaderService } from '../../_services/loader.service';
import { PlayerService } from '../../_services/player.service';
import { UserDataService } from '../../_services/UserData.service';

interface Player {
  name: string,
  dp: string,
  location: string,
  height: string,
  weight: string,
  age: string,
  positions: string[]
}

@Component({
  selector: 'app-player',
  templateUrl: './player.component.html',
  styleUrls: ['./player.component.css'],
  standalone: true,
  imports: [
    CommonModule
  ]
})
export class PlayerComponent implements OnInit{
  router = inject(Router);
  route = inject(ActivatedRoute);
  loadingService = inject(LoaderService);
  service = inject(PlayerService);
  userService = inject(UserDataService);

  id = "";

  player: Player | null = null

  tabContent: string[] = ["Overview"];
  selectedTabIndex = signal(0)

  ngOnInit(): void {
    this.route.params.subscribe((param) => {
      this.id = param['id'];

      this.loadingService.loadingOn();
      this.service.getInfo(this.id).subscribe((res) => {
        if (res['data']) {
          this.player = res['data']
        }
        this.loadingService.loadingOff();
      })

      this.generateTab();

      if (this.isMyPlayerProfile()) {
        this.loadingService.loadingOn();
        this.loadingService.loadingOff();
      }
    });
  }

  generateTab(): void {
    this.tabContent.push("Stats");
    this.tabContent.push("Timeline");
  }

  onTabSelect(tabIndex: number): void {
    this.selectedTabIndex.set(tabIndex)
  }

  isMyPlayerProfile(): boolean {
    return this.id === this.userService.getMyPlayerId();
  }
}
