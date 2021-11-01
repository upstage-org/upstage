export interface Connection<T> {
  pageInfo: PageInfo;
  edges: Edge<T>[];
  totalCount: number;
}

export interface Edge<T> {
  cursor: string;
  node: T;
}

export interface StudioGraph {
  mediaTypes: Connection<MediaType>;
  users: Connection<User>;
  stages: Connection<Stage>;
  media: Connection<Media>;
  whoami: User;
}

export interface PageInfo {
  startCursor: string;
  endCursor: string;
  hasNextPage: boolean;
  hasPreviousPage: boolean;
}

export interface MediaType {
  id: string;
  name: string;
}

export interface User {
  id: string;
  displayName: string;
  username: string;
  roleName: string;
}

export interface Stage {
  id: string;
  name: string;
  dbId: number;
}

export interface Media {
  id: string;
  name: string;
}
