export interface Result {
  data: Data;
}

export interface Data {
  assetList: AssetList;
}

export interface AssetList {
  edges: Edge[];
}

export interface Edge {
  node: Media;
}

export interface Media {
  id: string;
  name: string;
  description: string;
  assetType: AssetType;
  owner: Owner;
  createdOn: string;
  src: string;
  dbId: number;
  copyrightLevel: number;
  playerAccess: number[];
  permission: Permission;
  sign: string;
  stages: Stage[];
}

export interface AssetType {
  id: AssetTypeID;
  name: AssetTypeName;
}

export enum AssetTypeID {
  QXNzZXRUeXBlOjI = "QXNzZXRUeXBlOjI=",
  QXNzZXRUeXBlOjM = "QXNzZXRUeXBlOjM=",
  QXNzZXRUeXBlOjQ = "QXNzZXRUeXBlOjQ=",
  QXNzZXRUeXBlOjU = "QXNzZXRUeXBlOjU=",
  QXNzZXRUeXBlOjY = "QXNzZXRUeXBlOjY=",
  QXNzZXRUeXBlOjc = "QXNzZXRUeXBlOjc=",
  QXNzZXRUeXBlOjg = "QXNzZXRUeXBlOjg=",
}

export enum AssetTypeName {
  Audio = "audio",
  Avatar = "avatar",
  Backdrop = "backdrop",
  Curtain = "curtain",
  Prop = "prop",
  Shape = "shape",
  Stream = "stream",
}

export interface Owner {
  id: string;
  username: string;
  displayName: string;
}

export enum Permission {
  Editor = "editor",
  None = "none",
  Owner = "owner",
}

export interface Stage {
  id: number;
  name: string;
  url: URL;
}
