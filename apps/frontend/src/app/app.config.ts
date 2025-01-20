import { provideHttpClient } from '@angular/common/http';
import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';

import { provideAuth0 } from '@auth0/auth0-angular';

import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }), 
    provideRouter(routes),
    provideHttpClient(),
        provideAuth0({
          domain: 'dev-jasonhick.uk.auth0.com',
          clientId: 'Q30m5bqg5PUMwCm4SLPmMgF45VQrKhwx',
          authorizationParams: {
            redirect_uri: window.location.origin,
            audience: 'capstone-api',
            scope: 'openid profile email permissions'
          }
        }
      )
  ]
};
