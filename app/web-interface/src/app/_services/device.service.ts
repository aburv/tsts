import { Injectable } from '@angular/core';
import { LocalDataService } from './localStore.service';
import { DataService } from './data.service';

type Device = {
  deviceId: string,
  os: string,
  version: string,
  other: string,
  deviceType: string,
  platform: string,
}


@Injectable({
  providedIn: 'root',
})
export class DeviceService extends LocalDataService {
  constructor(
    private api: DataService
  ) {
    super('DIV_DA');
  }

  sendDeviceDetails(): void {
    if (this.getValues() === null) {
      const device = this.getDeviceInfo()
      this.api.post('device/register', device).subscribe((res) =>
        this.setValues({ deviceId: device["deviceId"], id: res["data"] })
      );
    }
  }

  getDeviceInfo(): Device {
    const info = navigator.userAgent
    let os = "unknown"
    let deviceType = "D"
    let osVersion = "unknown"

    if (/Windows NT (\d+\.\d+)/.exec(info)) {
      const winVersion = /Windows NT (\d+\.\d+)/.exec(info);
      osVersion = winVersion![1]
      os = "Windows"
      deviceType = 'D'
    }

    if (/Android/.test(info)) {
      os = "Android"
      if (/Mobile/.test(info)) {
        deviceType = 'P'
      }
      else{
        deviceType = 'T'
      }
    }
   
    if (/iPhone/.test(info)) {
      deviceType = 'P'
      os = "IOS"
    }
    if (/iPad/.test(info)) {
      deviceType = 'T'
      os = "IOS"
    }
    if (/Macintosh/.test(info)) {
      deviceType = 'D'
      os = "MacOS"
    }

    return {
      deviceId: "device_id",
      os: os,
      version: osVersion,
      other: info,
      deviceType: deviceType,
      platform: "B",
    }
  }

  getDeviceId(): string {
    return this.getValues()["id"];
  }

}
