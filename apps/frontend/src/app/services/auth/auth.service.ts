import { Injectable, inject } from '@angular/core';

import { AuthService as Auth0Service } from '@auth0/auth0-angular';
import { Observable, map, of, catchError } from 'rxjs';

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

  public getUserInfo(): Observable<any> {
    return this.auth0.user$;
  }

  public hasValidToken(): boolean {
    let isAuthenticated = false;
    this.auth0.isAuthenticated$.subscribe((auth) => {
      isAuthenticated = auth;
    });
    return isAuthenticated;
  }

  /**
   * Get all permissions from the JWT token's claims
   * @returns Observable of string array containing permissions
   */
  private getPermissions$(): Observable<string[]> {
    return this.auth0.getAccessTokenSilently().pipe(
      map((token) => {
        const decodedToken = this.parseJwt(token);
        return decodedToken?.permissions || [];
      }),
      catchError(() => of([]))
    );
  }

  /**
   * Parse a JWT token and return the payload
   */
  private parseJwt(token: string): any {
    try {
      if (!token) return {};
      // Split the token and get the payload part (second part)
      const base64Url = token.split('.')[1];
      if (!base64Url) return {};

      // Convert base64url to regular base64
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');

      // Decode and parse the JSON
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );

      return JSON.parse(jsonPayload);
    } catch (e) {
      return {};
    }
  }

  /**
   * Check if the user has a specific permission
   * @param permission The permission to check for
   * @returns Observable<boolean> indicating if the user has the permission
   */
  public hasPermission$(permission: string): Observable<boolean> {
    return this.getPermissions$().pipe(map((permissions) => permissions.includes(permission)));
  }

  /**
   * Check if the user has any of the specified permissions
   * @param permissions Array of permissions to check
   * @returns Observable<boolean> true if user has any of the permissions
   */
  public hasAnyPermission$(permissions: string[]): Observable<boolean> {
    return this.getPermissions$().pipe(
      map((userPermissions) => permissions.some((permission) => userPermissions.includes(permission)))
    );
  }

  /**
   * Check if the user has all of the specified permissions
   * @param permissions Array of permissions to check
   * @returns Observable<boolean> true if user has all permissions
   */
  public hasAllPermissions$(permissions: string[]): Observable<boolean> {
    return this.getPermissions$().pipe(
      map((userPermissions) => permissions.every((permission) => userPermissions.includes(permission)))
    );
  }
}
