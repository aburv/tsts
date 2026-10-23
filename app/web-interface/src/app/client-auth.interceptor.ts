import { inject } from '@angular/core';
import { HttpInterceptorFn } from '@angular/common/http';
import { from } from 'rxjs';
import { switchMap } from 'rxjs/operators';
import { ClientIdentityService } from './_services/client-identity.service';

export const clientAuthInterceptor: HttpInterceptorFn = (request, next) => {
    const identity = inject(ClientIdentityService);
    const serializedBody = request.serializeBody();
    const body = typeof serializedBody === 'string' ? serializedBody : null;
    return from(identity.getRequestHeaders(
        request.method,
        request.urlWithParams,
        body
    )).pipe(
        switchMap(headers => next(request.clone({ setHeaders: headers })))
    );
};
