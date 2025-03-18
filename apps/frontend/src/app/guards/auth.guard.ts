import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';

import { map, take } from 'rxjs/operators';

import { AuthService } from '@services';

export const AuthGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  return authService.isAuthenticated$.pipe(
    take(1),
    map((isAuthenticated) => {
      if (isAuthenticated) {
        return true;
      } else {
        router.navigate(['/login']);
        return false;
      }
    })
  );
};
