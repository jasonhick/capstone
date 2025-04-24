import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';

import { take } from 'rxjs';

import { ActorService } from '@services';
import { Actor, CreateActor, UpdateActor } from '../../../types/models';
import { HasPermissionDirective } from '../../../directives';
import { POST_ACTORS, PATCH_ACTORS } from '../../../auth/permissions';

@Component({
  selector: 'app-actor-form',
  standalone: true,
  imports: [CommonModule, FormsModule, HasPermissionDirective],
  templateUrl: './actor-form.component.html',
})
export class ActorFormComponent implements OnInit {
  private actorService = inject(ActorService);
  private route = inject(ActivatedRoute);
  private router = inject(Router);

  isEditMode = false;
  actorId: number | null = null;
  actor: CreateActor | UpdateActor = {
    name: '',
    age: 0,
    gender: '',
  };

  // Expose permission constant to the template
  protected POST_ACTORS = POST_ACTORS;
  protected PATCH_ACTORS = PATCH_ACTORS;

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id');
    if (id && id !== 'add') {
      this.isEditMode = true;
      this.actorId = Number(id);
      this.loadActorData();
    }
  }

  private loadActorData() {
    if (this.actorId) {
      this.actorService
        .getById(this.actorId)
        .pipe(take(1))
        .subscribe({
          next: (actor: Actor) => {
            this.actor = {
              name: actor.name,
              age: actor.age,
              gender: actor.gender,
              birth_date: actor.birth_date,
            };
          },
          error: (error: Error) => {
            console.error('Error fetching actor:', error);
          },
        });
    }
  }

  onSubmit() {
    if (this.isEditMode && this.actorId) {
      this.actorService
        .update(this.actorId, this.actor as UpdateActor)
        .pipe(take(1))
        .subscribe({
          next: () => {
            this.router.navigate(['/home/actors']);
          },
          error: (error: Error) => {
            console.error('Error updating actor:', error);
          },
        });
    } else {
      this.actorService
        .create(this.actor as CreateActor)
        .pipe(take(1))
        .subscribe({
          next: () => {
            this.router.navigate(['/home/actors']);
          },
          error: (error: Error) => {
            console.error('Error creating actor:', error);
          },
        });
    }
  }

  onBack() {
    this.router.navigate(['/home/actors']);
  }
}
