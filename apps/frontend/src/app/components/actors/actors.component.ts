import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';

import { take } from 'rxjs';

import { ActorService, Actor } from '@services';

@Component({
  selector: 'app-actors',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './actors.component.html',
})
export class ActorsComponent {
  private actorService = inject(ActorService);

  actors = signal<Actor[]>([]);

  ngOnInit() {
    this.actorService
      .getActors()
      .pipe(take(1))
      .subscribe(actors => {
        this.actors.set(actors);
      });
  }
}
