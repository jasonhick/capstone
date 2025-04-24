import { Directive, Input, OnInit, TemplateRef, ViewContainerRef, inject } from '@angular/core';
import { Subscription } from 'rxjs';

import { AuthService } from '@services';

/**
 * Structural directive that conditionally displays elements based on user permissions
 * Usage:
 * <div *hasPermission="'post:movies'">Add Movie</div>
 */
@Directive({
  selector: '[hasPermission]',
  standalone: true,
})
export class HasPermissionDirective implements OnInit {
  private authService = inject(AuthService);
  private templateRef = inject(TemplateRef<any>);
  private viewContainer = inject(ViewContainerRef);

  private subscription?: Subscription;
  private hasView = false;

  @Input({ required: true }) hasPermission = '';

  ngOnInit(): void {
    this.subscription = this.authService.hasPermission$(this.hasPermission).subscribe((hasPermission) => {
      if (hasPermission && !this.hasView) {
        this.viewContainer.createEmbeddedView(this.templateRef);
        this.hasView = true;
      } else if (!hasPermission && this.hasView) {
        this.viewContainer.clear();
        this.hasView = false;
      }
    });
  }

  ngOnDestroy(): void {
    this.subscription?.unsubscribe();
  }
}
