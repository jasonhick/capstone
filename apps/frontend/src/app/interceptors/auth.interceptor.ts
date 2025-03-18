import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';

import { mergeMap, catchError } from 'rxjs/operators';

import { AuthService } from '@services';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);

  // Only add the token for API requests
  if (req.url.includes('/api/v1/')) {
    return authService.getAccessToken$().pipe(
      mergeMap((token) => {
        // Clone the request and add the token
        const authReq = req.clone({
          setHeaders: {
            Authorization: `Bearer ${token}`,
          },
        });
        return next(authReq);
      }),
      catchError(() => {
        // If getting the token fails, proceed with the original request
        return next(req);
      })
    );
  }

  // Pass through other requests unchanged
  return next(req);
};
