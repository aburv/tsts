import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Config } from '../config';
import { Observable, of } from 'rxjs';
import { PingService } from './ping.service';

@Injectable({
  providedIn: 'root',
})
export class ImageService {
  constructor(
    private http: HttpClient,
    private pingService: PingService
  ) { }

  new(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file, file.name);

    const headers = {
      ...Config.getHeaders(),
    };
    delete headers.headers['content-type']

    if (!this.pingService.getIsServerDown()()) {
      return this.http.post((Config.getDomain() + "image/add"), formData, headers)
    }
    return of(null)
  }

  get(id: string, size: string): Observable<any> {
    return this.http.get(Config.getDomain() + 'image/' + id + "/" + size,
      {
        responseType: 'blob',
        ...Config.getHeaders(),
      }
    );
  }

}