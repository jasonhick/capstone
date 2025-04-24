import { Component, inject, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

import { take } from 'rxjs';

import { MovieService } from '@services';
import { Movie } from '../../types/models';
import { HasPermissionDirective } from '../../directives';
import { POST_MOVIES, PATCH_MOVIES, DELETE_MOVIES } from '../../auth/permissions';

@Component({
  selector: 'app-movies',
  standalone: true,
  imports: [CommonModule, HasPermissionDirective],
  templateUrl: './movies.component.html',
})
export class MoviesComponent implements OnInit {
  private movieService = inject(MovieService);
  private router = inject(Router);

  movies = signal<Movie[]>([]);

  // Expose permission constant to the template
  protected POST_MOVIES = POST_MOVIES;
  protected PATCH_MOVIES = PATCH_MOVIES;
  protected DELETE_MOVIES = DELETE_MOVIES;

  ngOnInit() {
    this.movieService
      .getAll()
      .pipe(take(1))
      .subscribe({
        next: (movies: Movie[]) => {
          this.movies.set(movies);
        },
        error: (error) => {
          console.error('Error fetching movies:', error);
        },
      });
  }

  onAddMovie() {
    this.router.navigate(['/home/movies/add']);
  }

  onEditMovie(movie: Movie) {
    this.router.navigate(['/home/movies', movie.id]);
  }

  onDeleteMovie(movie: Movie) {
    // TODO: Implement delete functionality
  }
}
