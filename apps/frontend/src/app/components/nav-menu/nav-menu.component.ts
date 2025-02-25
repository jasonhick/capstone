import { Component, inject } from '@angular/core';
import { RouterLink, RouterLinkActive, Router } from '@angular/router';
import { AuthService } from '@auth0/auth0-angular';

@Component({
  selector: 'app-nav-menu',
  standalone: true,
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './nav-menu.component.html',
})
export class NavMenuComponent {
  private router = inject(Router);
  private auth = inject(AuthService);

  logout() {
    this.auth.logout();
    this.router.navigate(['/']);
  }
}
