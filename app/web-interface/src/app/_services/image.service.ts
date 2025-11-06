import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Config } from '../config';
import { Observable, of, tap } from 'rxjs';
import { PingService } from './ping.service';

export interface ImageCache {
  [url: string]: ArrayBuffer;
}

@Injectable({
  providedIn: 'root',
})
export class ImageService {
  private http = inject(HttpClient);

  private static _cachedImages: ImageCache = {};

  getFromCache(url: string): ArrayBuffer | undefined {
    return ImageService._cachedImages[url]
  }

  setCache(url: string, data: ArrayBuffer): void {
    ImageService._cachedImages[url] = data
  }

  new(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file, file.name);

    const headers = {
      ...Config.getHeaders(),
    };
    delete headers.headers['content-type']

    if (!PingService.isServerDown()) {
      return this.http.post((Config.getDomain() + "image/add"), formData, headers)
    }
    return of(null)
  }

  getAndCachedImage(url: string): Observable<any> {
    const data = this.getFromCache(url);
    if (data) {
      return of(data);
    }
    return this.http.get(url,
      {
        responseType: 'blob',
        ...Config.getHeaders(),
      }
    ).pipe(tap(res => {
      this.setCache(url, res);
      return res;
    }));
  }

  get(id: string, size: string): Observable<any> {
    const url = Config.getDomain() + 'image/' + id + "/" + size;

    return this.getAndCachedImage(url);
  }
}
