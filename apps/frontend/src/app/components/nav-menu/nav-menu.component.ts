import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

import { LogoutButtonComponent } from '@components';

@Component({
  selector: 'app-nav-menu',
  standalone: true,
  imports: [RouterLink, RouterLinkActive, LogoutButtonComponent],
  templateUrl: './nav-menu.component.html',
})
export class NavMenuComponent {}
