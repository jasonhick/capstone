import { Injectable } from '@angular/core';
import { Actor, CreateActor, UpdateActor } from '../../types/models';
import { BaseService } from '../base.service';

@Injectable({
  providedIn: 'root',
})
export class ActorService extends BaseService<Actor, CreateActor, UpdateActor> {
  protected override endpoint = 'actors';
}
