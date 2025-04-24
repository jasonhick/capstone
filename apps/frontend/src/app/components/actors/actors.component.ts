import { Component, inject, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

import { take } from 'rxjs';

import { ActorService } from '@services';
import { Actor } from '../../types/models';
import { HasPermissionDirective } from '../../directives';
import { POST_ACTORS, PATCH_ACTORS, DELETE_ACTORS } from '../../auth/permissions';

@Component({
  selector: 'app-actors',
  standalone: true,
  imports: [CommonModule, HasPermissionDirective],
  templateUrl: './actors.component.html',
})
export class ActorsComponent implements OnInit {
  private actorService = inject(ActorService);
  private router = inject(Router);

  actors = signal<Actor[]>([]);

  // Expose permission constant to the template
  protected POST_ACTORS = POST_ACTORS;
  protected PATCH_ACTORS = PATCH_ACTORS;
  protected DELETE_ACTORS = DELETE_ACTORS;

  ngOnInit() {
    this.actorService
      .getAll()
      .pipe(take(1))
      .subscribe({
        next: (actors: Actor[]) => {
          this.actors.set(actors);
        },
        error: (error) => {
          console.error('Error fetching actors:', error);
        },
      });
  }

  onAddActor() {
    this.router.navigate(['/home/actors/add']);
  }

  onEditActor(actor: Actor) {
    this.router.navigate(['/home/actors', actor.id]);
  }

  onDeleteActor(actor: Actor) {
    // TODO: Implement delete functionality
  }
}
