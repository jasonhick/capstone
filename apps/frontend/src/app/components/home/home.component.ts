import { Component } from '@angular/core';
import { MovieService } from '../../services/movies/movies.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="container mx-auto p-4">
      <h1 class="text-2xl font-bold mb-4">Welcome to Movies App</h1>
      <p>You are now logged in!</p>
    </div>
  `,
})
export class HomeComponent {
  constructor() {}
}
