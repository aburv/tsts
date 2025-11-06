import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AuthUserService } from '../../_services/auth-user.service';
import { UserDataService } from '../../_services/UserData.service';
import { AppUser, GAuthUser } from '../../_models/user';
import { DeviceService } from '../../_services/device.service';

import { Config } from '../../config';

import { DialogComponent } from '../dialog/dialog.component';
import { ImageComponent } from '../image/image.component';
import { Icon } from '../icon/icon.component';

declare const google: any;

@Component({
  selector: 'app-user-button',
  standalone: true,
  imports: [
    CommonModule,
    DialogComponent,
    ImageComponent
  ],
  templateUrl: './user-button.component.html',
  styleUrls: ['./user-button.component.css']
})
export class UserButtonComponent implements OnInit {
  private authUser = inject(AuthUserService);
  private serviceData = inject(UserDataService);
  private deviceService = inject(DeviceService);

  readonly Icon = Icon

  user: AppUser | null = null;

  location: {
    "lat": number,
    "long": number
  } | null = null;

  isDialogOn = false;

  ngOnInit(): void {
    this.authUser.getLoggedUser().subscribe((user: GAuthUser | null) => {
      if (user !== null) {
        this.userLogin(user);
      }
    });

    this.serviceData.autoSignIn().subscribe(async (hasUser) => {
      if (hasUser) {
        this.setCurrentUser();
      }
      else {
        await this.loadGoogleClient();
        this.initializeGoogleSignIn();
      }
    });
  }

  loadGoogleClient(): Promise<any> {
    return new Promise((resolve) => {
      const checkGoogle = () => {
        if (window['google'] && google.accounts) {
          resolve(google);
        } else {
          setTimeout(checkGoogle, 50);
        }
      };
      checkGoogle();
    });
  }

  initializeGoogleSignIn() {
    google.accounts.id.initialize({
      client_id: Config.getGCID(),
      callback: (response: any) => this.authUser.handleGoogleResponse(response)
    });

    google.accounts.id.renderButton(
      document.getElementById('google-signin-button'),
      {
        type: 'icon',
        theme: 'outline',
        size: 'large',
        shape: 'pill'
      }
    );

    google.accounts.id.prompt();
  }

  userLogin(user: GAuthUser): void {
    this.getLocation();
    const data = {
      user: {
        uId: {
          gId: user.sub,
          value: user.email,
          type: "M"
        },
        name: user.name,
        picUrl: user.picture,
      },
      login: {
        deviceId: this.deviceService.getDeviceId(),
        location: this.location
      }
    };
    this.serviceData.signIn(data).subscribe((res: boolean) => {
      if (res) {
        this.setCurrentUser()
      }
    })
  }

  getLocation() {
    navigator.geolocation.getCurrentPosition(this.setLocation.bind(this));
  }

  setLocation(position: GeolocationPosition): void {
    this.location = {
      "lat": position.coords.latitude,
      "long": position.coords.longitude
    }
  }

  setCurrentUser(): void {
    this.user = this.serviceData.getUser();
    document.getElementById('google-signin-button')!.style.visibility = 'hidden';
  }
}