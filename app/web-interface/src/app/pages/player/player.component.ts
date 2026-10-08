import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Title } from '@angular/platform-browser';
import { ImageComponent } from '../../components/image/image.component';
import { Icon } from '../../components/icon/icon.component';
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
    CommonModule,
    ImageComponent,
  ]
})
export class PlayerComponent implements OnDestroy, OnInit {
  readonly Icon = Icon;

  title = inject(Title);
  router = inject(Router);
  route = inject(ActivatedRoute);
  loadingService = inject(LoaderService);
  service = inject(PlayerService);
  userService = inject(UserDataService);

  id = "";

  player: WritableSignal<Player | null> = signal(null);

  tabContent: string[] = ["Overview"];
  selectedTabIndex = signal(0)

  ngOnInit(): void {
    this.route.params.subscribe((param) => {
      this.id = param['id'];

      this.loadingService.loadingOn();
      this.service.getInfo(this.id).subscribe({
        next: (res) => {
          if (res?.data) {
            this.player.set(res.data);
          } else {
            this.player.set(null);
          }
          this.title.setTitle((this.player()?.name || 'Player') + ' | Takbuff');
          this.loadingService.loadingOff();
        },
        error: (error) => {
          this.player.set(null);
          this.loadingService.loadingOff();
        }
      });

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
