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
  tags: Connection<Tag>;
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
  dbId: number;
  displayName: string;
  username: string;
  roleName: string;
}

export interface Stage {
  id: string;
  name: string;
  dbId: number;
}

export interface Tag {
  id: string;
  name: string;
  dbId: number;
}

export interface AssignedStage {
  id: number
  name: string
  url: string
}

export interface Media {
  id: string;
  name: string;
  src: string;
  description: string;
  createdOn: string;
  size: number;
  copyrightLevel: number;
  assetType: MediaType;
  owner: User;
  stages: AssignedStage[];
  tags: string[];
}

export interface MediaAttributes {
  multi: boolean;
  frames: string[];
  voice: Voice;
  link: Link;
  w: number;
  h: number;
}

export interface Link {
  blank: boolean;
  url: string;
}

export interface Voice {
}

export interface UploadFile {
  action?: string;
  filename?: string;
  data?: any;
  file: File;
  headers?: any;
  withCredentials?: boolean;
  method?: string;
  id: number;
  preview: string;
  status: 'local' | 'uploaded';
  url?: string;
}