import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';

import { take } from 'rxjs';

import { MovieService, Movie } from '@services';

@Component({
  selector: 'app-movies',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './movies.component.html',
})
export class MoviesComponent {
  private movieService = inject(MovieService);

  movies = signal<Movie[]>([]);

  ngOnInit() {
    this.movieService
      .getMovies()
      .pipe(take(1))
      .subscribe((movies) => {
        this.movies.set(movies);
      });
  }
}
