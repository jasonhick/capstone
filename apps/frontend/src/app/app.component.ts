import { Component, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { LoginButtonComponent } from './components/login-button/login-button.component';
import { AuthService } from '@auth0/auth0-angular';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, LoginButtonComponent],
  templateUrl: './app.component.html',
})
export class AppComponent {
  private auth = inject(AuthService);
  isAuthenticated$ = this.auth.isAuthenticated$;
}
