import { Component, inject } from '@angular/core';
import { AuthService } from '@services';

@Component({
  selector: 'app-logout-button',
  standalone: true,
  templateUrl: './logout-button.component.html',
})
export class LogoutButtonComponent {
  private authService = inject(AuthService);

  logout(): void {
    this.authService.logout();
  }
}
