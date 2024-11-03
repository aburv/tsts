import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { DataService } from './data.service';


@Injectable({
  providedIn: 'root',
})
export class SearchService {
  constructor(private api: DataService) { }

  get(text: string): Observable<any> {
    return this.api.get('search/'+ text)
  }
}
