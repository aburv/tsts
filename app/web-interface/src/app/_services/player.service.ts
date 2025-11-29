import { Injectable, inject } from '@angular/core';
import { Observable, of } from 'rxjs';
import { DataService } from './data.service';

@Injectable({
    providedIn: 'root',
})
export class PlayerService {
    private api = inject(DataService);

    getInfo(id: string): Observable<any> {
        return this.api.get('player/' + id);
    }

}
