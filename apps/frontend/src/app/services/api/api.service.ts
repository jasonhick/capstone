import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '@env/environment';
import { AuthService } from '@services';

// Define interfaces here since there are no models
interface Actor {
  id?: number;
  name: string;
  age: number;
  gender: string;
  birthdate?: string;
}

interface Movie {
  id?: number;
  title: string;
  release_date: string;
}

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private http = inject(HttpClient);
  private authService = inject(AuthService);
  private apiUrl = environment.apiUrl;

  private getAuthHeaders() {
    return {
      headers: {
        Authorization: `Bearer ${this.authService.getAccessToken()}`,
      },
    };
  }

  // Actors
  getActors(): Observable<Actor[]> {
    return this.http.get<Actor[]>(`${this.apiUrl}/actors`);
  }

  createActor(actor: Partial<Actor>): Observable<any> {
    return this.http.post(`${this.apiUrl}/actors`, actor, this.getAuthHeaders());
  }

  updateActor(id: number, actor: Partial<Actor>): Observable<any> {
    return this.http.patch(`${this.apiUrl}/actors/${id}`, actor, this.getAuthHeaders());
  }

  deleteActor(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/actors/${id}`, this.getAuthHeaders());
  }

  // Movies
  getMovies(): Observable<Movie[]> {
    return this.http.get<Movie[]>(`${this.apiUrl}/movies`);
  }

  createMovie(movie: Partial<Movie>): Observable<any> {
    return this.http.post(`${this.apiUrl}/movies`, movie, this.getAuthHeaders());
  }

  updateMovie(id: number, movie: Partial<Movie>): Observable<any> {
    return this.http.patch(`${this.apiUrl}/movies/${id}`, movie, this.getAuthHeaders());
  }

  deleteMovie(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/movies/${id}`, this.getAuthHeaders());
  }

  // Relationships
  addActorToMovie(movieId: number, actorId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/movies/${movieId}/actors`, { actor_id: actorId }, this.getAuthHeaders());
  }
}
