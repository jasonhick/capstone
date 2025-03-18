import { Component, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Observable } from 'rxjs';

import { LoginButtonComponent } from '@components';
import { AuthService } from '@services';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, LoginButtonComponent],
  templateUrl: './app.component.html',
})
export class AppComponent {
  private authService = inject(AuthService);
  isAuthenticated$: Observable<boolean> = this.authService.isAuthenticated$;
}
