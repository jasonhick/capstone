import { Component, inject } from '@angular/core';

import { AuthService } from '@services';

@Component({
  selector: 'app-login-button',
  standalone: true,
  templateUrl: './login-button.component.html',
})
export class LoginButtonComponent {
  private authService = inject(AuthService);

  login() {
    this.authService.login();
  }
}
