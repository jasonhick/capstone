import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { LoginButtonComponent } from './components/login-button/login-button.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, LoginButtonComponent],
  template: `
    <app-login-button></app-login-button>
    <router-outlet></router-outlet>
  `,
})
export class AppComponent {
  title = 'Movie App';
}
