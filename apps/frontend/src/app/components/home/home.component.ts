import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';

import { NavMenuComponent } from '@components';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterOutlet, NavMenuComponent],
  template: `
    <div class="min-h-screen flex flex-col">
      <app-nav-menu></app-nav-menu>
      <main class="container mx-auto p-4 flex-grow">
        <router-outlet></router-outlet>
      </main>
    </div>
  `,
})
export class HomeComponent {
  constructor() {}
}
