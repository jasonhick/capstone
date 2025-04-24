import { Injectable } from '@angular/core';
import { Movie, CreateMovie, UpdateMovie } from '../../types/models';
import { BaseService } from '../base.service';

@Injectable({
  providedIn: 'root',
})
export class MovieService extends BaseService<Movie, CreateMovie, UpdateMovie> {
  protected override endpoint = 'movies';
}
