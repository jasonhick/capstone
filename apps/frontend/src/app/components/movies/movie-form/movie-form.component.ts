import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';

import { take } from 'rxjs';

import { MovieService } from '@services';
import { Movie, CreateMovie, UpdateMovie } from '../../../types/models';
import { HasPermissionDirective } from '../../../directives';
import { POST_MOVIES, PATCH_MOVIES } from '../../../auth/permissions';

@Component({
  selector: 'app-movie-form',
  standalone: true,
  imports: [CommonModule, FormsModule, HasPermissionDirective],
  templateUrl: './movie-form.component.html',
})
export class MovieFormComponent implements OnInit {
  private movieService = inject(MovieService);
  private route = inject(ActivatedRoute);
  private router = inject(Router);

  isEditMode = false;
  movieId: number | null = null;
  movie: CreateMovie | UpdateMovie = {
    title: '',
    release_date: '',
  };

  // Expose permission constant to the template
  protected POST_MOVIES = POST_MOVIES;
  protected PATCH_MOVIES = PATCH_MOVIES;

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id');
    if (id && id !== 'add') {
      this.isEditMode = true;
      this.movieId = Number(id);
      this.loadMovieData();
    }
  }

  private loadMovieData() {
    if (this.movieId) {
      this.movieService
        .getById(this.movieId)
        .pipe(take(1))
        .subscribe({
          next: (movie: Movie) => {
            this.movie = {
              title: movie.title,
              release_date: movie.release_date,
            };
          },
          error: (error: Error) => {
            console.error('Error fetching movie:', error);
          },
        });
    }
  }

  onSubmit() {
    if (this.isEditMode && this.movieId) {
      this.movieService
        .update(this.movieId, this.movie as UpdateMovie)
        .pipe(take(1))
        .subscribe({
          next: () => {
            this.router.navigate(['/home/movies']);
          },
          error: (error: Error) => {
            console.error('Error updating movie:', error);
          },
        });
    } else {
      this.movieService
        .create(this.movie as CreateMovie)
        .pipe(take(1))
        .subscribe({
          next: () => {
            this.router.navigate(['/home/movies']);
          },
          error: (error: Error) => {
            console.error('Error creating movie:', error);
          },
        });
    }
  }

  onBack() {
    this.router.navigate(['/home/movies']);
  }
}
