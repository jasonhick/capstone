import { HttpClient } from '@angular/common/http';
import { inject } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '@env/environment';

export abstract class BaseService<T, CreateDTO, UpdateDTO> {
  protected http = inject(HttpClient);
  protected abstract endpoint: string;

  protected get apiUrl(): string {
    return `${environment.apiUrl}/${this.endpoint}`;
  }

  getAll(): Observable<T[]> {
    return this.http.get<T[]>(this.apiUrl);
  }

  getById(id: number): Observable<T> {
    return this.http.get<T>(`${this.apiUrl}/${id}`);
  }

  create(data: CreateDTO): Observable<T> {
    return this.http.post<T>(this.apiUrl, data);
  }

  update(id: number, data: UpdateDTO): Observable<T> {
    return this.http.patch<T>(`${this.apiUrl}/${id}`, data);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }
}
