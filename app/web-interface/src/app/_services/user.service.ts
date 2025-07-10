import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { DataService } from './data.service';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  constructor(private api: DataService) { }

  getUserData(): Observable<any> {
    return this.api.get('user/app')
  }
}
