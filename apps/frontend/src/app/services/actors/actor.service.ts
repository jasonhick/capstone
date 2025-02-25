import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';

import { environment } from '@env/environment';

export interface Actor {
  id?: number;
  name: string;
  birth_date: string;
}

@Injectable({
  providedIn: 'root',
})
export class ActorService {
  private apiUrl = `${environment.apiUrl}/actors`;

  private http = inject(HttpClient);

  // Get all actors
  getActors(): Observable<Actor[]> {
    return this.http.get<Actor[]>(this.apiUrl);
  }

  // Get a single actor by ID
  getActor(id: number): Observable<Actor> {
    return this.http.get<Actor>(`${this.apiUrl}/${id}`);
  }

  // Create a new actor
  createActor(actor: Actor): Observable<Actor> {
    return this.http.post<Actor>(this.apiUrl, actor);
  }

  // Update an actor
  updateActor(id: number, actor: Actor): Observable<Actor> {
    return this.http.patch<Actor>(`${this.apiUrl}/${id}`, actor);
  }

  // Delete an actor
  deleteActor(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }
}
