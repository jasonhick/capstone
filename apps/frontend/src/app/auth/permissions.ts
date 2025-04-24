/**
 * Permission constants for role-based access control
 * These must match the permissions defined in Auth0 and the backend
 */

// Actor permissions
export const GET_ACTORS = 'get:actors';
export const POST_ACTORS = 'post:actors';
export const PATCH_ACTORS = 'patch:actors';
export const DELETE_ACTORS = 'delete:actors';

// Movie permissions
export const GET_MOVIES = 'get:movies';
export const POST_MOVIES = 'post:movies';
export const PATCH_MOVIES = 'patch:movies';
export const DELETE_MOVIES = 'delete:movies';

// Role-based permission sets
export const CASTING_ASSISTANT_PERMISSIONS = [GET_ACTORS, GET_MOVIES];

export const CASTING_DIRECTOR_PERMISSIONS = [
  ...CASTING_ASSISTANT_PERMISSIONS,
  POST_ACTORS,
  PATCH_ACTORS,
  DELETE_ACTORS,
  PATCH_MOVIES,
];

export const EXECUTIVE_PRODUCER_PERMISSIONS = [...CASTING_DIRECTOR_PERMISSIONS, POST_MOVIES, DELETE_MOVIES];
