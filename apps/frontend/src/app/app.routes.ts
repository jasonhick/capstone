import { Routes } from '@angular/router';


export const routes: Routes = [
    { path: 'actors', loadComponent: () => import('./components/actors/actors.component').then(m => m.ActorsComponent) },
    { path: 'movies', loadComponent: () => import('./components/movies/movies.component').then(m => m.MoviesComponent) }
];
