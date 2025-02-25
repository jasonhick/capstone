import { Component, inject } from '@angular/core';

import { AuthService } from '@auth0/auth0-angular';

@Component({
  selector: 'app-login-button',
  imports: [],
  templateUrl: './login-button.component.html',
})
export class LoginButtonComponent {
  public auth = inject(AuthService);
}
