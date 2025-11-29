import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { LoaderService } from 'src/app/_services/loader.service';
import { PlayerService } from 'src/app/_services/player.service';
import { UserDataService } from 'src/app/_services/UserData.service';
import { timeout } from 'rxjs';

type Player = {
  name: string,
  dp: string,
  location: string,
  height: string,
  weight: string,
  age: string,
  positions: Array<string>
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

  tabContent: Array<string> = ["Overview"];
  selectedTabIndex = signal(0)

  constructor() { }

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
