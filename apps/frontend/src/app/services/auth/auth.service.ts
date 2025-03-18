import { Injectable, inject } from '@angular/core';

import { AuthService as Auth0Service } from '@auth0/auth0-angular';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private auth0 = inject(Auth0Service);

  public get isAuthenticated$(): Observable<boolean> {
    return this.auth0.isAuthenticated$;
  }

  public login(): void {
    this.auth0.loginWithRedirect({
      appState: { target: '/home' },
    });
  }

  public logout(): void {
    this.auth0.logout({
      logoutParams: {
        returnTo: window.location.origin + '/login',
      },
    });
  }

  public getAccessToken(): string {
    let token = '';
    // Use a synchronous approach to get the token when needed
    this.auth0.getAccessTokenSilently().subscribe((accessToken) => {
      token = accessToken;
    });
    return token;
  }

  public getAccessToken$(): Observable<string> {
    return this.auth0.getAccessTokenSilently();
  }

  public getUserInfo(): any {
    return this.auth0.user$;
  }

  public hasValidToken(): boolean {
    let isAuthenticated = false;
    this.auth0.isAuthenticated$.subscribe((auth) => {
      isAuthenticated = auth;
    });
    return isAuthenticated;
  }
}
