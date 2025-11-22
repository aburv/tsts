import { Injectable, signal, inject } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Config } from '../config';

function getPingUrl(): string {
  return Config.getDomain() + 'ping/';
}

@Injectable({
  providedIn: 'root',
})
export class PingService {
  private http = inject(HttpClient);

  static isServerDown = signal<boolean>(false);

  ping(): void {
    const url = getPingUrl();
    this.http.post(url, Config.getHeaders()).subscribe({
      next: () => {
        PingService.isServerDown.set(false);
      },
      error: (error: HttpErrorResponse) => {
        if (error.status === 404 || error.status === 0) {
          PingService.isServerDown.set(true);
        } else {
          PingService.isServerDown.set(false);
        }
      }
    });
  }
}
