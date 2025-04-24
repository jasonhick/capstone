import { Routes } from '@angular/router';
import { AuthGuard } from './guards/auth.guard';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full',
  },
  {
    path: 'home',
    loadComponent: () => import('./components/home/home.component').then((m) => m.HomeComponent),
    canActivate: [AuthGuard],
    children: [
      {
        path: 'actors',
        loadComponent: () => import('./components/actors/actors.component').then((m) => m.ActorsComponent),
      },
      {
        path: 'actors/add',
        loadComponent: () =>
          import('./components/actors/actor-form/actor-form.component').then((m) => m.ActorFormComponent),
      },
      {
        path: 'actors/:id',
        loadComponent: () =>
          import('./components/actors/actor-form/actor-form.component').then((m) => m.ActorFormComponent),
      },
      {
        path: 'movies',
        loadComponent: () => import('./components/movies/movies.component').then((m) => m.MoviesComponent),
      },
      {
        path: 'movies/add',
        loadComponent: () =>
          import('./components/movies/movie-form/movie-form.component').then((m) => m.MovieFormComponent),
      },
      {
        path: 'movies/:id',
        loadComponent: () =>
          import('./components/movies/movie-form/movie-form.component').then((m) => m.MovieFormComponent),
      },
    ],
  },
];
