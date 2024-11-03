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
    const info = window.navigator.userAgent
    let os = "unknown"
    let deviceType = "Desktop"
    let osVersion = "unknown"

    if (/Windows NT (\d+\.\d+)/.exec(info)) {
      const winVersion = /Windows NT (\d+\.\d+)/.exec(info);
      osVersion = winVersion![1]
      os = "Windows"
      deviceType = 'Desktop'
    }

    if (/Android/.test(info)) {
      os = "Android"
      if (/Mobile/.test(info)) {
        deviceType = 'Phone'
      }
      else{
        deviceType = 'Tab'
      }
    }
   
    if (/iPhone/.test(info)) {
      deviceType = 'Phone'
      os = "IOS"
    }
    if (/iPad/.test(info)) {
      deviceType = 'Tab'
      os = "IOS"
    }
    if (/Macintosh/.test(info)) {
      deviceType = 'Desktop'
      os = "MacOS"
    }

    return {
      deviceId: "device_id",
      os: os,
      version: osVersion,
      other: info,
      deviceType: deviceType,
      platform: "Browser",
    }
  }
}