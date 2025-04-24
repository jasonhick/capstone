export interface Actor {
  id: number;
  name: string;
  age: number;
  gender: string;
  birth_date?: string;
}

export interface Movie {
  id: number;
  title: string;
  release_date: string;
  actors: Actor[];
}

// Create types using Omit
export type CreateActor = Omit<Actor, 'id'>;
export type CreateMovie = Omit<Movie, 'id' | 'actors'>;

// Update types using Partial
export type UpdateActor = Partial<CreateActor>;
export type UpdateMovie = Partial<CreateMovie> & {
  actors?: number[]; // Array of actor IDs for updates
};
