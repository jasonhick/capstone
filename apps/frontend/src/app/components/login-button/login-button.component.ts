import { Component, inject } from '@angular/core';
import { AuthService } from '@auth0/auth0-angular';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login-button',
  standalone: true,
  templateUrl: './login-button.component.html',
})
export class LoginButtonComponent {
  private auth = inject(AuthService);
  private router = inject(Router);

  login() {
    this.auth.loginWithRedirect({
      appState: { target: '/home/movies' },
    });

    // Subscribe to auth state changes to handle the redirect
    this.auth.isAuthenticated$.subscribe((isAuthenticated) => {
      if (isAuthenticated) {
        this.router.navigate(['/home/movies']);
      }
    });
  }
}
