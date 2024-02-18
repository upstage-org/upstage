// @ts-nocheck
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type Scalars = {
  ID: string;
  Boolean: boolean;
  String: string;
  DateTime: any;
  Int: number;
  Float: number;
  Date: any;
};

export interface Query {
  node: Node | null;
  mediaTypes: AssetTypeConnection | null;
  tags: TagConnection | null;
  users: UserConnection | null;
  media: AssetConnection | null;
  stages: StageConnection | null;
  adminPlayers: AdminPlayerConnection | null;
  /** Logged in user info */
  whoami: User | null;
  notifications: (Notification | null)[] | null;
  voices: (Voice | null)[] | null;
  __typename: "Query";
}

/** An object with an ID */
export type Node = (
  | AssetType
  | Tag
  | User
  | Asset
  | AssetUsage
  | Stage
  | AdminPlayer
  | Notification
  | Voice
) & { __isUnion?: true };

export interface AssetTypeConnection {
  /** Pagination data for this connection. */
  pageInfo: PageInfo;
  /** Contains the nodes in this connection. */
  edges: (AssetTypeEdge | null)[];
  __typename: "AssetTypeConnection";
}

/** The Relay compliant `PageInfo` type, containing data necessary to paginate this connection. */
export interface PageInfo {
  /** When paginating forwards, are there more items? */
  hasNextPage: Scalars["Boolean"];
  /** When paginating backwards, are there more items? */
  hasPreviousPage: Scalars["Boolean"];
  /** When paginating backwards, the cursor to continue. */
  startCursor: Scalars["String"] | null;
  /** When paginating forwards, the cursor to continue. */
  endCursor: Scalars["String"] | null;
  __typename: "PageInfo";
}

/** A Relay edge containing a `AssetType` and its cursor. */
export interface AssetTypeEdge {
  /** The item at the end of the edge */
  node: AssetType | null;
  /** A cursor for use in pagination */
  cursor: Scalars["String"];
  __typename: "AssetTypeEdge";
}

export interface AssetType {
  /** The ID of the object. */
  id: Scalars["ID"];
  name: Scalars["String"];
  description: Scalars["String"] | null;
  fileLocation: Scalars["String"];
  createdOn: Scalars["DateTime"];
  /** Database ID */
  dbId: Scalars["Int"] | null;
  __typename: "AssetType";
}

/** An enumeration. */
export type AssetTypeSortEnum =
  | "ID_ASC"
  | "ID_DESC"
  | "NAME_ASC"
  | "NAME_DESC"
  | "DESCRIPTION_ASC"
  | "DESCRIPTION_DESC"
  | "FILE_LOCATION_ASC"
  | "FILE_LOCATION_DESC"
  | "CREATED_ON_ASC"
  | "CREATED_ON_DESC";

export interface TagConnection {
  /** Pagination data for this connection. */
  pageInfo: PageInfo;
  /** Contains the nodes in this connection. */
  edges: (TagEdge | null)[];
  __typename: "TagConnection";
}

/** A Relay edge containing a `Tag` and its cursor. */
export interface TagEdge {
  /** The item at the end of the edge */
  node: Tag | null;
  /** A cursor for use in pagination */
  cursor: Scalars["String"];
  __typename: "TagEdge";
}

export interface Tag {
  /** The ID of the object. */
  id: Scalars["ID"];
  name: Scalars["String"];
  color: Scalars["String"] | null;
  createdOn: Scalars["DateTime"];
  /** Database ID */
  dbId: Scalars["Int"] | null;
  __typename: "Tag";
}

/** An enumeration. */
export type TagSortEnum =
  | "ID_ASC"
  | "ID_DESC"
  | "NAME_ASC"
  | "NAME_DESC"
  | "COLOR_ASC"
  | "COLOR_DESC"
  | "CREATED_ON_ASC"
  | "CREATED_ON_DESC";

export interface UserConnection {
  /** Pagination data for this connection. */
  pageInfo: PageInfo;
  /** Contains the nodes in this connection. */
  edges: (UserEdge | null)[];
  __typename: "UserConnection";
}

/** A Relay edge containing a `User` and its cursor. */
export interface UserEdge {
  /** The item at the end of the edge */
  node: User | null;
  /** A cursor for use in pagination */
  cursor: Scalars["String"];
  __typename: "UserEdge";
}

export interface User {
  /** The ID of the object. */
  id: Scalars["ID"];
  username: Scalars["String"];
  password: Scalars["String"];
  email: Scalars["String"] | null;
  binName: Scalars["String"] | null;
  role: Scalars["Int"];
  firstName: Scalars["String"] | null;
  lastName: Scalars["String"] | null;
  displayName: Scalars["String"] | null;
  active: Scalars["Boolean"];
  createdOn: Scalars["DateTime"] | null;
  firebasePushnotId: Scalars["String"] | null;
  deactivatedOn: Scalars["DateTime"] | null;
  uploadLimit: Scalars["Int"] | null;
  intro: Scalars["String"] | null;
  canSendEmail: Scalars["Boolean"] | null;
  lastLogin: Scalars["DateTime"] | null;
  /** Database ID */
  dbId: Scalars["Int"] | null;
  /** Name of the role */
  roleName: Scalars["String"] | null;
  __typename: "User";
}

/** An enumeration. */
export type UserSortEnum =
  | "ID_ASC"
  | "ID_DESC"
  | "USERNAME_ASC"
  | "USERNAME_DESC"
  | "PASSWORD_ASC"
  | "PASSWORD_DESC"
  | "EMAIL_ASC"
  | "EMAIL_DESC"
  | "BIN_NAME_ASC"
  | "BIN_NAME_DESC"
  | "ROLE_ASC"
  | "ROLE_DESC"
  | "FIRST_NAME_ASC"
  | "FIRST_NAME_DESC"
  | "LAST_NAME_ASC"
  | "LAST_NAME_DESC"
  | "DISPLAY_NAME_ASC"
  | "DISPLAY_NAME_DESC"
  | "ACTIVE_ASC"
  | "ACTIVE_DESC"
  | "CREATED_ON_ASC"
  | "CREATED_ON_DESC"
  | "FIREBASE_PUSHNOT_ID_ASC"
  | "FIREBASE_PUSHNOT_ID_DESC"
  | "DEACTIVATED_ON_ASC"
  | "DEACTIVATED_ON_DESC"
  | "UPLOAD_LIMIT_ASC"
  | "UPLOAD_LIMIT_DESC"
  | "INTRO_ASC"
  | "INTRO_DESC"
  | "CAN_SEND_EMAIL_ASC"
  | "CAN_SEND_EMAIL_DESC"
  | "LAST_LOGIN_ASC"
  | "LAST_LOGIN_DESC";

export interface AssetConnection {
  /** Pagination data for this connection. */
  pageInfo: PageInfo;
  /** Contains the nodes in this connection. */
  edges: (AssetEdge | null)[];
  totalCount: Scalars["Int"] | null;
  __typename: "AssetConnection";
}

/** A Relay edge containing a `Asset` and its cursor. */
export interface AssetEdge {
  /** The item at the end of the edge */
  node: Asset | null;
  /** A cursor for use in pagination */
  cursor: Scalars["String"];
  __typename: "AssetEdge";
}

export interface Asset {
  /** The ID of the object. */
  id: Scalars["ID"];
  name: Scalars["String"];
  assetTypeId: Scalars["Int"];
  ownerId: Scalars["Int"];
  description: Scalars["String"] | null;
  fileLocation: Scalars["String"];
  createdOn: Scalars["DateTime"];
  updatedOn: Scalars["DateTime"];
  size: Scalars["Float"];
  copyrightLevel: Scalars["Int"];
  assetType: AssetType | null;
  owner: User | null;
  /** Stages that this media is assigned to */
  stages: (AssignedStage | null)[] | null;
  /** Media tags */
  tags: (Scalars["String"] | null)[] | null;
  /** Users who had been granted or acknowledged to use this media */
  permissions: (AssetUsage | null)[] | null;
  /** Database ID */
  dbId: Scalars["Int"] | null;
  /** Logical path of the media */
  src: Scalars["String"] | null;
  /** Permission of the logged in user for this media */
  privilege: Previlege | null;
  /** Stream sign that is required to publish from broadcaster */
  sign: Scalars["String"] | null;
  __typename: "Asset";
}

export interface AssignedStage {
  id: Scalars["Int"] | null;
  name: Scalars["String"] | null;
  url: Scalars["String"] | null;
  __typename: "AssignedStage";
}

export interface AssetUsage {
  /** The ID of the object. */
  id: Scalars["ID"];
  assetId: Scalars["Int"];
  userId: Scalars["Int"];
  approved: Scalars["Boolean"];
  seen: Scalars["Boolean"];
  note: Scalars["String"] | null;
  createdOn: Scalars["DateTime"];
  user: User | null;
  asset: Asset | null;
  __typename: "AssetUsage";
}

export type Previlege =
  | "NONE"
  | "OWNER"
  | "APPROVED"
  | "PENDING_APPROVAL"
  | "REQUIRE_APPROVAL";

/** An enumeration. */
export type AssetSortEnum =
  | "ID_ASC"
  | "ID_DESC"
  | "NAME_ASC"
  | "NAME_DESC"
  | "ASSET_TYPE_ID_ASC"
  | "ASSET_TYPE_ID_DESC"
  | "OWNER_ID_ASC"
  | "OWNER_ID_DESC"
  | "DESCRIPTION_ASC"
  | "DESCRIPTION_DESC"
  | "FILE_LOCATION_ASC"
  | "FILE_LOCATION_DESC"
  | "CREATED_ON_ASC"
  | "CREATED_ON_DESC"
  | "UPDATED_ON_ASC"
  | "UPDATED_ON_DESC"
  | "SIZE_ASC"
  | "SIZE_DESC"
  | "COPYRIGHT_LEVEL_ASC"
  | "COPYRIGHT_LEVEL_DESC";

export interface StageConnection {
  /** Pagination data for this connection. */
  pageInfo: PageInfo;
  /** Contains the nodes in this connection. */
  edges: (StageEdge | null)[];
  totalCount: Scalars["Int"] | null;
  __typename: "StageConnection";
}

/** A Relay edge containing a `Stage` and its cursor. */
export interface StageEdge {
  /** The item at the end of the edge */
  node: Stage | null;
  /** A cursor for use in pagination */
  cursor: Scalars["String"];
  __typename: "StageEdge";
}

export interface Stage {
  /** The ID of the object. */
  id: Scalars["ID"];
  name: Scalars["String"];
  description: Scalars["String"] | null;
  ownerId: Scalars["Int"];
  fileLocation: Scalars["String"];
  createdOn: Scalars["DateTime"];
  lastAccess: Scalars["DateTime"] | null;
  cover: Scalars["String"] | null;
  visibility: Scalars["String"] | null;
  status: Scalars["String"] | null;
  owner: User | null;
  attributes: (StageAttributes | null)[] | null;
  /** Database ID */
  dbId: Scalars["Int"] | null;
  /** Player access to this stage */
  permission: Scalars["String"] | null;
  __typename: "Stage";
}

export interface StageAttributes {
  id: Scalars["Float"];
  stageId: Scalars["Int"];
  name: Scalars["String"];
  description: Scalars["String"];
  createdOn: Scalars["DateTime"];
  stage: Stage | null;
  __typename: "StageAttributes";
}

/** An enumeration. */
export type StageSortEnum =
  | "ID_ASC"
  | "ID_DESC"
  | "NAME_ASC"
  | "NAME_DESC"
  | "DESCRIPTION_ASC"
  | "DESCRIPTION_DESC"
  | "OWNER_ID_ASC"
  | "OWNER_ID_DESC"
  | "FILE_LOCATION_ASC"
  | "FILE_LOCATION_DESC"
  | "CREATED_ON_ASC"
  | "CREATED_ON_DESC"
  | "LAST_ACCESS_ASC"
  | "LAST_ACCESS_DESC";

export interface AdminPlayerConnection {
  /** Pagination data for this connection. */
  pageInfo: PageInfo;
  /** Contains the nodes in this connection. */
  edges: (AdminPlayerEdge | null)[];
  totalCount: Scalars["Int"] | null;
  __typename: "AdminPlayerConnection";
}

/** A Relay edge containing a `AdminPlayer` and its cursor. */
export interface AdminPlayerEdge {
  /** The item at the end of the edge */
  node: AdminPlayer | null;
  /** A cursor for use in pagination */
  cursor: Scalars["String"];
  __typename: "AdminPlayerEdge";
}

export interface AdminPlayer {
  /** The ID of the object. */
  id: Scalars["ID"];
  username: Scalars["String"];
  password: Scalars["String"];
  email: Scalars["String"] | null;
  binName: Scalars["String"] | null;
  role: Scalars["Int"];
  firstName: Scalars["String"] | null;
  lastName: Scalars["String"] | null;
  displayName: Scalars["String"] | null;
  active: Scalars["Boolean"];
  createdOn: Scalars["DateTime"] | null;
  firebasePushnotId: Scalars["String"] | null;
  deactivatedOn: Scalars["DateTime"] | null;
  uploadLimit: Scalars["Int"] | null;
  intro: Scalars["String"] | null;
  canSendEmail: Scalars["Boolean"] | null;
  /** Last login time */
  lastLogin: Scalars["DateTime"] | null;
  /** Database ID */
  dbId: Scalars["Int"] | null;
  /** Player access to this user */
  permission: Scalars["String"] | null;
  /** Name of the role */
  roleName: Scalars["String"] | null;
  __typename: "AdminPlayer";
}

/** An enumeration. */
export type AdminPlayerSortEnum =
  | "ID_ASC"
  | "ID_DESC"
  | "USERNAME_ASC"
  | "USERNAME_DESC"
  | "PASSWORD_ASC"
  | "PASSWORD_DESC"
  | "EMAIL_ASC"
  | "EMAIL_DESC"
  | "BIN_NAME_ASC"
  | "BIN_NAME_DESC"
  | "ROLE_ASC"
  | "ROLE_DESC"
  | "FIRST_NAME_ASC"
  | "FIRST_NAME_DESC"
  | "LAST_NAME_ASC"
  | "LAST_NAME_DESC"
  | "DISPLAY_NAME_ASC"
  | "DISPLAY_NAME_DESC"
  | "ACTIVE_ASC"
  | "ACTIVE_DESC"
  | "CREATED_ON_ASC"
  | "CREATED_ON_DESC"
  | "FIREBASE_PUSHNOT_ID_ASC"
  | "FIREBASE_PUSHNOT_ID_DESC"
  | "DEACTIVATED_ON_ASC"
  | "DEACTIVATED_ON_DESC"
  | "UPLOAD_LIMIT_ASC"
  | "UPLOAD_LIMIT_DESC"
  | "INTRO_ASC"
  | "INTRO_DESC"
  | "CAN_SEND_EMAIL_ASC"
  | "CAN_SEND_EMAIL_DESC"
  | "LAST_LOGIN_ASC"
  | "LAST_LOGIN_DESC";

export interface Notification {
  /** The ID of the object. */
  id: Scalars["ID"];
  /** Type of notification */
  type: NotificationType | null;
  /** If notification is of type media usage, this object contain the permission request */
  mediaUsage: AssetUsage | null;
  __typename: "Notification";
}

export type NotificationType = "MEDIA_USAGE";

export interface Voice {
  /** The ID of the object. */
  id: Scalars["ID"];
  /** The voice */
  voice: VoiceOutput | null;
  /** The avatar owned this voice */
  avatar: Asset | null;
  __typename: "Voice";
}

export interface VoiceOutput {
  /** Voice name */
  voice: Scalars["String"] | null;
  /** Voice variant */
  variant: Scalars["String"];
  /** Voice pitch, range from 0 to 100 */
  pitch: Scalars["Int"];
  /** Voice speed, range from 0 to 350 */
  speed: Scalars["Int"];
  /** Voice amplitude, range from 0 to 100 */
  amplitude: Scalars["Int"];
  __typename: "VoiceOutput";
}

export interface Mutation {
  /** Mutation to assign stages to a media. */
  calcSizes: CalcSizes | null;
  /** Mutation to delete a media. */
  deleteMedia: DeleteMedia | null;
  /** Mutation to upload a media. */
  uploadFile: UploadFile | null;
  /** Mutation to upload a media. */
  saveMedia: SaveMedia | null;
  authUser: AuthMutation | null;
  refreshUser: RefreshMutation | null;
  /** Mutation to approve or reject a media usage request */
  confirmPermission: ConfirmPermission | null;
  /** Mutation to create an asset usage */
  requestPermission: RequestPermission | null;
  /** Mutation to assign a stage to a media */
  quickAssignMutation: QuickAssignMutation | null;
  /** Mutation to update a stage status attribute. */
  updateStatus: UpdateAttributeStatus | null;
  /** Mutation to update a stage visibility attribute. */
  updateVisibility: UpdateAttributeVisibility | null;
  /** Update a user. */
  updateUser: UpdateUser | null;
  deleteUser: DeleteUser | null;
  /** Mutation to create a user. */
  batchUserCreation: BatchUserCreation | null;
  /** Mutation to customise foyer. */
  sendEmail: SendEmail | null;
  changePassword: ChangePassword | null;
  __typename: "Mutation";
}

/** Mutation to assign stages to a media. */
export interface CalcSizes {
  /** Total calculated sizes */
  size: Scalars["Int"] | null;
  __typename: "CalcSizes";
}

/** Mutation to delete a media. */
export interface DeleteMedia {
  success: Scalars["Boolean"] | null;
  message: Scalars["String"] | null;
  __typename: "DeleteMedia";
}

/** Mutation to upload a media. */
export interface UploadFile {
  /** Uploaded file url */
  url: Scalars["String"] | null;
  __typename: "UploadFile";
}

/** Mutation to upload a media. */
export interface SaveMedia {
  /** Media saved by this mutation. */
  asset: Asset | null;
  __typename: "SaveMedia";
}

export interface AuthMutation {
  accessToken: Scalars["String"] | null;
  refreshToken: Scalars["String"] | null;
  __typename: "AuthMutation";
}

export interface RefreshMutation {
  newToken: Scalars["String"] | null;
  __typename: "RefreshMutation";
}

/** Mutation to approve or reject a media usage request */
export interface ConfirmPermission {
  /** Success */
  success: Scalars["Boolean"] | null;
  /** Reason for why the mutation failed */
  message: Scalars["String"] | null;
  /** Permissions that were updated */
  permissions: (AssetUsage | null)[] | null;
  __typename: "ConfirmPermission";
}

/** Mutation to create an asset usage */
export interface RequestPermission {
  /** Success */
  success: Scalars["Boolean"] | null;
  __typename: "RequestPermission";
}

/** Mutation to assign a stage to a media */
export interface QuickAssignMutation {
  /** Success */
  success: Scalars["Boolean"] | null;
  /** Reason for why the mutation failed */
  message: Scalars["String"] | null;
  __typename: "QuickAssignMutation";
}

/** Mutation to update a stage status attribute. */
export interface UpdateAttributeStatus {
  result: Scalars["String"] | null;
  __typename: "UpdateAttributeStatus";
}

/** Mutation to update a stage visibility attribute. */
export interface UpdateAttributeVisibility {
  result: Scalars["String"] | null;
  __typename: "UpdateAttributeVisibility";
}

/** Update a user. */
export interface UpdateUser {
  /** User updated by this mutation. */
  user: AdminPlayer | null;
  __typename: "UpdateUser";
}

export interface DeleteUser {
  /** Password changed successful or not */
  success: Scalars["Boolean"] | null;
  __typename: "DeleteUser";
}

/** Mutation to create a user. */
export interface BatchUserCreation {
  /** Users created by this mutation. */
  users: (AdminPlayer | null)[] | null;
  __typename: "BatchUserCreation";
}

/** Mutation to customise foyer. */
export interface SendEmail {
  /** True if the config was saved. */
  success: Scalars["Boolean"] | null;
  __typename: "SendEmail";
}

export interface ChangePassword {
  /** Password changed successful or not */
  success: Scalars["Boolean"] | null;
  __typename: "ChangePassword";
}

export interface QueryGenqlSelection {
  node?: NodeGenqlSelection & {
    __args: {
      /** The ID of the object */
      id: Scalars["ID"];
    };
  };
  mediaTypes?: AssetTypeConnectionGenqlSelection & {
    __args?: {
      sort?: (AssetTypeSortEnum | null)[] | null;
      before?: Scalars["String"] | null;
      after?: Scalars["String"] | null;
      first?: Scalars["Int"] | null;
      last?: Scalars["Int"] | null;
    };
  };
  tags?: TagConnectionGenqlSelection & {
    __args?: {
      sort?: (TagSortEnum | null)[] | null;
      before?: Scalars["String"] | null;
      after?: Scalars["String"] | null;
      first?: Scalars["Int"] | null;
      last?: Scalars["Int"] | null;
    };
  };
  users?: UserConnectionGenqlSelection & {
    __args?: {
      active?: Scalars["Boolean"] | null;
      sort?: (UserSortEnum | null)[] | null;
      before?: Scalars["String"] | null;
      after?: Scalars["String"] | null;
      first?: Scalars["Int"] | null;
      last?: Scalars["Int"] | null;
    };
  };
  media?: AssetConnectionGenqlSelection & {
    __args?: {
      id?: Scalars["ID"] | null;
      nameLike?: Scalars["String"] | null;
      createdBetween?: (Scalars["Date"] | null)[] | null;
      fileLocation?: Scalars["String"] | null;
      mediaTypes?: (Scalars["String"] | null)[] | null;
      owners?: (Scalars["String"] | null)[] | null;
      stages?: (Scalars["Int"] | null)[] | null;
      tags?: (Scalars["String"] | null)[] | null;
      sort?: (AssetSortEnum | null)[] | null;
      before?: Scalars["String"] | null;
      after?: Scalars["String"] | null;
      first?: Scalars["Int"] | null;
      last?: Scalars["Int"] | null;
    };
  };
  stages?: StageConnectionGenqlSelection & {
    __args?: {
      id?: Scalars["ID"] | null;
      nameLike?: Scalars["String"] | null;
      createdBetween?: (Scalars["Date"] | null)[] | null;
      fileLocation?: Scalars["String"] | null;
      owners?: (Scalars["String"] | null)[] | null;
      sort?: (StageSortEnum | null)[] | null;
      before?: Scalars["String"] | null;
      after?: Scalars["String"] | null;
      first?: Scalars["Int"] | null;
      last?: Scalars["Int"] | null;
    };
  };
  adminPlayers?: AdminPlayerConnectionGenqlSelection & {
    __args?: {
      id?: Scalars["ID"] | null;
      usernameLike?: Scalars["String"] | null;
      createdBetween?: (Scalars["Date"] | null)[] | null;
      role?: Scalars["Int"] | null;
      sort?: (AdminPlayerSortEnum | null)[] | null;
      before?: Scalars["String"] | null;
      after?: Scalars["String"] | null;
      first?: Scalars["Int"] | null;
      last?: Scalars["Int"] | null;
    };
  };
  /** Logged in user info */
  whoami?: UserGenqlSelection;
  notifications?: NotificationGenqlSelection;
  voices?: VoiceGenqlSelection;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

/** An object with an ID */
export interface NodeGenqlSelection {
  /** The ID of the object. */
  id?: boolean | number;
  on_AssetType?: AssetTypeGenqlSelection;
  on_Tag?: TagGenqlSelection;
  on_User?: UserGenqlSelection;
  on_Asset?: AssetGenqlSelection;
  on_AssetUsage?: AssetUsageGenqlSelection;
  on_Stage?: StageGenqlSelection;
  on_AdminPlayer?: AdminPlayerGenqlSelection;
  on_Notification?: NotificationGenqlSelection;
  on_Voice?: VoiceGenqlSelection;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

export interface AssetTypeConnectionGenqlSelection {
  /** Pagination data for this connection. */
  pageInfo?: PageInfoGenqlSelection;
  /** Contains the nodes in this connection. */
  edges?: AssetTypeEdgeGenqlSelection;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

/** The Relay compliant `PageInfo` type, containing data necessary to paginate this connection. */
export interface PageInfoGenqlSelection {
  /** When paginating forwards, are there more items? */
  hasNextPage?: boolean | number;
  /** When paginating backwards, are there more items? */
  hasPreviousPage?: boolean | number;
  /** When paginating backwards, the cursor to continue. */
  startCursor?: boolean | number;
  /** When paginating forwards, the cursor to continue. */
  endCursor?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

/** A Relay edge containing a `AssetType` and its cursor. */
export interface AssetTypeEdgeGenqlSelection {
  /** The item at the end of the edge */
  node?: AssetTypeGenqlSelection;
  /** A cursor for use in pagination */
  cursor?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

export interface AssetTypeGenqlSelection {
  /** The ID of the object. */
  id?: boolean | number;
  name?: boolean | number;
  description?: boolean | number;
  fileLocation?: boolean | number;
  createdOn?: boolean | number;
  /** Database ID */
  dbId?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

export interface TagConnectionGenqlSelection {
  /** Pagination data for this connection. */
  pageInfo?: PageInfoGenqlSelection;
  /** Contains the nodes in this connection. */
  edges?: TagEdgeGenqlSelection;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

/** A Relay edge containing a `Tag` and its cursor. */
export interface TagEdgeGenqlSelection {
  /** The item at the end of the edge */
  node?: TagGenqlSelection;
  /** A cursor for use in pagination */
  cursor?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

export interface TagGenqlSelection {
  /** The ID of the object. */
  id?: boolean | number;
  name?: boolean | number;
  color?: boolean | number;
  createdOn?: boolean | number;
  /** Database ID */
  dbId?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

export interface UserConnectionGenqlSelection {
  /** Pagination data for this connection. */
  pageInfo?: PageInfoGenqlSelection;
  /** Contains the nodes in this connection. */
  edges?: UserEdgeGenqlSelection;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

/** A Relay edge containing a `User` and its cursor. */
export interface UserEdgeGenqlSelection {
  /** The item at the end of the edge */
  node?: UserGenqlSelection;
  /** A cursor for use in pagination */
  cursor?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

export interface UserGenqlSelection {
  /** The ID of the object. */
  id?: boolean | number;
  username?: boolean | number;
  password?: boolean | number;
  email?: boolean | number;
  binName?: boolean | number;
  role?: boolean | number;
  firstName?: boolean | number;
  lastName?: boolean | number;
  displayName?: boolean | number;
  active?: boolean | number;
  createdOn?: boolean | number;
  firebasePushnotId?: boolean | number;
  deactivatedOn?: boolean | number;
  uploadLimit?: boolean | number;
  intro?: boolean | number;
  canSendEmail?: boolean | number;
  lastLogin?: boolean | number;
  /** Database ID */
  dbId?: boolean | number;
  /** Name of the role */
  roleName?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

export interface AssetConnectionGenqlSelection {
  /** Pagination data for this connection. */
  pageInfo?: PageInfoGenqlSelection;
  /** Contains the nodes in this connection. */
  edges?: AssetEdgeGenqlSelection;
  totalCount?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

/** A Relay edge containing a `Asset` and its cursor. */
export interface AssetEdgeGenqlSelection {
  /** The item at the end of the edge */
  node?: AssetGenqlSelection;
  /** A cursor for use in pagination */
  cursor?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

export interface AssetGenqlSelection {
  /** The ID of the object. */
  id?: boolean | number;
  name?: boolean | number;
  assetTypeId?: boolean | number;
  ownerId?: boolean | number;
  description?: boolean | number;
  fileLocation?: boolean | number;
  createdOn?: boolean | number;
  updatedOn?: boolean | number;
  size?: boolean | number;
  copyrightLevel?: boolean | number;
  assetType?: AssetTypeGenqlSelection;
  owner?: UserGenqlSelection;
  /** Stages that this media is assigned to */
  stages?: AssignedStageGenqlSelection;
  /** Media tags */
  tags?: boolean | number;
  /** Users who had been granted or acknowledged to use this media */
  permissions?: AssetUsageGenqlSelection;
  /** Database ID */
  dbId?: boolean | number;
  /** Logical path of the media */
  src?: boolean | number;
  /** Permission of the logged in user for this media */
  privilege?: boolean | number;
  /** Stream sign that is required to publish from broadcaster */
  sign?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

export interface AssignedStageGenqlSelection {
  id?: boolean | number;
  name?: boolean | number;
  url?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

export interface AssetUsageGenqlSelection {
  /** The ID of the object. */
  id?: boolean | number;
  assetId?: boolean | number;
  userId?: boolean | number;
  approved?: boolean | number;
  seen?: boolean | number;
  note?: boolean | number;
  createdOn?: boolean | number;
  user?: UserGenqlSelection;
  asset?: AssetGenqlSelection;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

export interface StageConnectionGenqlSelection {
  /** Pagination data for this connection. */
  pageInfo?: PageInfoGenqlSelection;
  /** Contains the nodes in this connection. */
  edges?: StageEdgeGenqlSelection;
  totalCount?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

/** A Relay edge containing a `Stage` and its cursor. */
export interface StageEdgeGenqlSelection {
  /** The item at the end of the edge */
  node?: StageGenqlSelection;
  /** A cursor for use in pagination */
  cursor?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

export interface StageGenqlSelection {
  /** The ID of the object. */
  id?: boolean | number;
  name?: boolean | number;
  description?: boolean | number;
  ownerId?: boolean | number;
  fileLocation?: boolean | number;
  createdOn?: boolean | number;
  lastAccess?: boolean | number;
  cover?: boolean | number;
  visibility?: boolean | number;
  status?: boolean | number;
  owner?: UserGenqlSelection;
  attributes?: StageAttributesGenqlSelection;
  /** Database ID */
  dbId?: boolean | number;
  /** Player access to this stage */
  permission?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

export interface StageAttributesGenqlSelection {
  id?: boolean | number;
  stageId?: boolean | number;
  name?: boolean | number;
  description?: boolean | number;
  createdOn?: boolean | number;
  stage?: StageGenqlSelection;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

export interface AdminPlayerConnectionGenqlSelection {
  /** Pagination data for this connection. */
  pageInfo?: PageInfoGenqlSelection;
  /** Contains the nodes in this connection. */
  edges?: AdminPlayerEdgeGenqlSelection;
  totalCount?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

/** A Relay edge containing a `AdminPlayer` and its cursor. */
export interface AdminPlayerEdgeGenqlSelection {
  /** The item at the end of the edge */
  node?: AdminPlayerGenqlSelection;
  /** A cursor for use in pagination */
  cursor?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

export interface AdminPlayerGenqlSelection {
  /** The ID of the object. */
  id?: boolean | number;
  username?: boolean | number;
  password?: boolean | number;
  email?: boolean | number;
  binName?: boolean | number;
  role?: boolean | number;
  firstName?: boolean | number;
  lastName?: boolean | number;
  displayName?: boolean | number;
  active?: boolean | number;
  createdOn?: boolean | number;
  firebasePushnotId?: boolean | number;
  deactivatedOn?: boolean | number;
  uploadLimit?: boolean | number;
  intro?: boolean | number;
  canSendEmail?: boolean | number;
  /** Last login time */
  lastLogin?: boolean | number;
  /** Database ID */
  dbId?: boolean | number;
  /** Player access to this user */
  permission?: boolean | number;
  /** Name of the role */
  roleName?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

export interface NotificationGenqlSelection {
  /** The ID of the object. */
  id?: boolean | number;
  /** Type of notification */
  type?: boolean | number;
  /** If notification is of type media usage, this object contain the permission request */
  mediaUsage?: AssetUsageGenqlSelection;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

export interface VoiceGenqlSelection {
  /** The ID of the object. */
  id?: boolean | number;
  /** The voice */
  voice?: VoiceOutputGenqlSelection;
  /** The avatar owned this voice */
  avatar?: AssetGenqlSelection;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

export interface VoiceOutputGenqlSelection {
  /** Voice name */
  voice?: boolean | number;
  /** Voice variant */
  variant?: boolean | number;
  /** Voice pitch, range from 0 to 100 */
  pitch?: boolean | number;
  /** Voice speed, range from 0 to 350 */
  speed?: boolean | number;
  /** Voice amplitude, range from 0 to 100 */
  amplitude?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

export interface MutationGenqlSelection {
  /** Mutation to assign stages to a media. */
  calcSizes?: CalcSizesGenqlSelection;
  /** Mutation to delete a media. */
  deleteMedia?: DeleteMediaGenqlSelection & {
    __args: {
      /** Global Id of the asset to be deleted. */
      id: Scalars["ID"];
    };
  };
  /** Mutation to upload a media. */
  uploadFile?: UploadFileGenqlSelection & {
    __args: {
      /** Base64 encoded content of the uploading media */
      base64: Scalars["String"];
      /** Original file name */
      filename: Scalars["String"];
    };
  };
  /** Mutation to upload a media. */
  saveMedia?: SaveMediaGenqlSelection & { __args: { input: SaveMediaInput } };
  authUser?: AuthMutationGenqlSelection & {
    __args?: {
      password?: Scalars["String"] | null;
      username?: Scalars["String"] | null;
    };
  };
  refreshUser?: RefreshMutationGenqlSelection & {
    __args?: { refreshToken?: Scalars["String"] | null };
  };
  /** Mutation to approve or reject a media usage request */
  confirmPermission?: ConfirmPermissionGenqlSelection & {
    __args?: {
      /** Whether the permission is approved. True for approving, False for rejecting */
      approved?: Scalars["Boolean"] | null;
      /** ID of the media usage request */
      id?: Scalars["ID"] | null;
    };
  };
  /** Mutation to create an asset usage */
  requestPermission?: RequestPermissionGenqlSelection & {
    __args?: {
      /** ID of the media usage request */
      assetId?: Scalars["ID"] | null;
      /** Note for the media usage request */
      note?: Scalars["String"] | null;
    };
  };
  /** Mutation to assign a stage to a media */
  quickAssignMutation?: QuickAssignMutationGenqlSelection & {
    __args?: {
      /** ID of the media */
      id?: Scalars["ID"] | null;
      /** ID of the stage */
      stageId?: Scalars["Int"] | null;
    };
  };
  /** Mutation to update a stage status attribute. */
  updateStatus?: UpdateAttributeStatusGenqlSelection & {
    __args: {
      /** Global Id of the stage. */
      stageId: Scalars["ID"];
    };
  };
  /** Mutation to update a stage visibility attribute. */
  updateVisibility?: UpdateAttributeVisibilityGenqlSelection & {
    __args: {
      /** Global Id of the stage. */
      stageId: Scalars["ID"];
    };
  };
  /** Update a user. */
  updateUser?: UpdateUserGenqlSelection & {
    __args: { inbound: UpdateUserInput };
  };
  deleteUser?: DeleteUserGenqlSelection & {
    __args: { inbound: DeleteUserInput };
  };
  /** Mutation to create a user. */
  batchUserCreation?: BatchUserCreationGenqlSelection & {
    __args: {
      stageIds?: (Scalars["Int"] | null)[] | null;
      users: (BatchUserInput | null)[];
    };
  };
  /** Mutation to customise foyer. */
  sendEmail?: SendEmailGenqlSelection & {
    __args: {
      /** The bcc recipients of the email. Comma separated. */
      bcc?: Scalars["String"] | null;
      /** The body of the email. HTML is allowed. */
      body: Scalars["String"];
      /** The recipients of the email. Comma separated. */
      recipients: Scalars["String"];
      /** The subject of the email. */
      subject: Scalars["String"];
    };
  };
  changePassword?: ChangePasswordGenqlSelection & {
    __args: { inbound: ChangePasswordInput };
  };
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

/** Mutation to assign stages to a media. */
export interface CalcSizesGenqlSelection {
  /** Total calculated sizes */
  size?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

/** Mutation to delete a media. */
export interface DeleteMediaGenqlSelection {
  success?: boolean | number;
  message?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

/** Mutation to upload a media. */
export interface UploadFileGenqlSelection {
  /** Uploaded file url */
  url?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

/** Mutation to upload a media. */
export interface SaveMediaGenqlSelection {
  /** Media saved by this mutation. */
  asset?: AssetGenqlSelection;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

/** Arguments to update a stage. */
export interface SaveMediaInput {
  /** Name of the media */
  name: Scalars["String"];
  /** Uploaded url of files */
  urls?: (Scalars["String"] | null)[] | null;
  /** Avatar/prop/backdrop,... default to just a generic media */
  mediaType?: Scalars["String"] | null;
  /** ID of the media (for updating) */
  id?: Scalars["ID"] | null;
  /** Copyright level */
  copyrightLevel?: Scalars["Int"] | null;
  /** Owner of the media, in case of uploading for someone else */
  owner?: Scalars["String"] | null;
  /** Users who can access and edit this media */
  userIds?: (Scalars["Int"] | null)[] | null;
  /** Id of stages to be assigned to */
  stageIds?: (Scalars["Int"] | null)[] | null;
  /** Media tags */
  tags?: (Scalars["String"] | null)[] | null;
  /** Width of the media */
  w?: Scalars["Int"] | null;
  /** Height of the media */
  h?: Scalars["Int"] | null;
  /** It would be useful to have a 'Notes' field on the permissions tab, where i could note the actual copyright owner when it's not me, and other information such as what the image is of, when or where taken, this kind of thing. */
  note?: Scalars["String"] | null;
  /** Voice settings */
  voice?: AvatarVoiceInput | null;
  /** On click action link */
  link?: LinkInput | null;
}

export interface AvatarVoiceInput {
  /** Voice name */
  voice?: Scalars["String"] | null;
  /** Voice variant */
  variant: Scalars["String"];
  /** Voice pitch, range from 0 to 100 */
  pitch: Scalars["Int"];
  /** Voice speed, range from 0 to 350 */
  speed: Scalars["Int"];
  /** Voice amplitude, range from 0 to 100 */
  amplitude: Scalars["Int"];
}

export interface LinkInput {
  /** Link url */
  url: Scalars["String"];
  /** Open in new tab? */
  blank: Scalars["Boolean"];
  /** Link effect */
  effect: Scalars["Boolean"];
}

export interface AuthMutationGenqlSelection {
  accessToken?: boolean | number;
  refreshToken?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

export interface RefreshMutationGenqlSelection {
  newToken?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

/** Mutation to approve or reject a media usage request */
export interface ConfirmPermissionGenqlSelection {
  /** Success */
  success?: boolean | number;
  /** Reason for why the mutation failed */
  message?: boolean | number;
  /** Permissions that were updated */
  permissions?: AssetUsageGenqlSelection;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

/** Mutation to create an asset usage */
export interface RequestPermissionGenqlSelection {
  /** Success */
  success?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

/** Mutation to assign a stage to a media */
export interface QuickAssignMutationGenqlSelection {
  /** Success */
  success?: boolean | number;
  /** Reason for why the mutation failed */
  message?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

/** Mutation to update a stage status attribute. */
export interface UpdateAttributeStatusGenqlSelection {
  result?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

/** Mutation to update a stage visibility attribute. */
export interface UpdateAttributeVisibilityGenqlSelection {
  result?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

/** Update a user. */
export interface UpdateUserGenqlSelection {
  /** User updated by this mutation. */
  user?: AdminPlayerGenqlSelection;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

/** Arguments to update a user. */
export interface UpdateUserInput {
  /** Username */
  username?: Scalars["String"] | null;
  /** Password */
  password?: Scalars["String"] | null;
  /** Email Address */
  email?: Scalars["String"] | null;
  /** bin_name */
  binName?: Scalars["String"] | null;
  /** User Role */
  role?: Scalars["Int"] | null;
  /** First Name */
  firstName?: Scalars["String"] | null;
  /** Last Name */
  lastName?: Scalars["String"] | null;
  /** Display Name */
  displayName?: Scalars["String"] | null;
  /** Active record or not */
  active?: Scalars["Boolean"] | null;
  /** firebase_pushnot_id */
  firebasePushnotId?: Scalars["String"] | null;
  /** Maximum file upload size limit, in bytes */
  uploadLimit?: Scalars["Int"] | null;
  /** Introduction */
  intro?: Scalars["String"] | null;
  /** Global Id of the user. */
  id: Scalars["ID"];
}

export interface DeleteUserGenqlSelection {
  /** Password changed successful or not */
  success?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

/** Arguments to update a user. */
export interface DeleteUserInput {
  /** Username */
  username?: Scalars["String"] | null;
  /** Password */
  password?: Scalars["String"] | null;
  /** Email Address */
  email?: Scalars["String"] | null;
  /** bin_name */
  binName?: Scalars["String"] | null;
  /** User Role */
  role?: Scalars["Int"] | null;
  /** First Name */
  firstName?: Scalars["String"] | null;
  /** Last Name */
  lastName?: Scalars["String"] | null;
  /** Display Name */
  displayName?: Scalars["String"] | null;
  /** Active record or not */
  active?: Scalars["Boolean"] | null;
  /** firebase_pushnot_id */
  firebasePushnotId?: Scalars["String"] | null;
  /** Maximum file upload size limit, in bytes */
  uploadLimit?: Scalars["Int"] | null;
  /** Introduction */
  intro?: Scalars["String"] | null;
  /** Global Id of the user. */
  id: Scalars["ID"];
}

/** Mutation to create a user. */
export interface BatchUserCreationGenqlSelection {
  /** Users created by this mutation. */
  users?: AdminPlayerGenqlSelection;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

export interface BatchUserInput {
  username: Scalars["String"];
  email: Scalars["String"];
  password: Scalars["String"];
}

/** Mutation to customise foyer. */
export interface SendEmailGenqlSelection {
  /** True if the config was saved. */
  success?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

export interface ChangePasswordGenqlSelection {
  /** Password changed successful or not */
  success?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

/** Arguments to update a user. */
export interface ChangePasswordInput {
  /** Username */
  username?: Scalars["String"] | null;
  /** Password */
  password?: Scalars["String"] | null;
  /** Email Address */
  email?: Scalars["String"] | null;
  /** bin_name */
  binName?: Scalars["String"] | null;
  /** User Role */
  role?: Scalars["Int"] | null;
  /** First Name */
  firstName?: Scalars["String"] | null;
  /** Last Name */
  lastName?: Scalars["String"] | null;
  /** Display Name */
  displayName?: Scalars["String"] | null;
  /** Active record or not */
  active?: Scalars["Boolean"] | null;
  /** firebase_pushnot_id */
  firebasePushnotId?: Scalars["String"] | null;
  /** Maximum file upload size limit, in bytes */
  uploadLimit?: Scalars["Int"] | null;
  /** Introduction */
  intro?: Scalars["String"] | null;
  /** Global Id of the user. */
  id: Scalars["ID"];
  oldPassword: Scalars["String"];
  newPassword: Scalars["String"];
}

const Query_possibleTypes: string[] = ["Query"];
export const isQuery = (obj?: { __typename?: any } | null): obj is Query => {
  if (!obj?.__typename) throw new Error('__typename is missing in "isQuery"');
  return Query_possibleTypes.includes(obj.__typename);
};

const Node_possibleTypes: string[] = [
  "AssetType",
  "Tag",
  "User",
  "Asset",
  "AssetUsage",
  "Stage",
  "AdminPlayer",
  "Notification",
  "Voice",
];
export const isNode = (obj?: { __typename?: any } | null): obj is Node => {
  if (!obj?.__typename) throw new Error('__typename is missing in "isNode"');
  return Node_possibleTypes.includes(obj.__typename);
};

const AssetTypeConnection_possibleTypes: string[] = ["AssetTypeConnection"];
export const isAssetTypeConnection = (
  obj?: { __typename?: any } | null,
): obj is AssetTypeConnection => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isAssetTypeConnection"');
  return AssetTypeConnection_possibleTypes.includes(obj.__typename);
};

const PageInfo_possibleTypes: string[] = ["PageInfo"];
export const isPageInfo = (
  obj?: { __typename?: any } | null,
): obj is PageInfo => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isPageInfo"');
  return PageInfo_possibleTypes.includes(obj.__typename);
};

const AssetTypeEdge_possibleTypes: string[] = ["AssetTypeEdge"];
export const isAssetTypeEdge = (
  obj?: { __typename?: any } | null,
): obj is AssetTypeEdge => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isAssetTypeEdge"');
  return AssetTypeEdge_possibleTypes.includes(obj.__typename);
};

const AssetType_possibleTypes: string[] = ["AssetType"];
export const isAssetType = (
  obj?: { __typename?: any } | null,
): obj is AssetType => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isAssetType"');
  return AssetType_possibleTypes.includes(obj.__typename);
};

const TagConnection_possibleTypes: string[] = ["TagConnection"];
export const isTagConnection = (
  obj?: { __typename?: any } | null,
): obj is TagConnection => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isTagConnection"');
  return TagConnection_possibleTypes.includes(obj.__typename);
};

const TagEdge_possibleTypes: string[] = ["TagEdge"];
export const isTagEdge = (
  obj?: { __typename?: any } | null,
): obj is TagEdge => {
  if (!obj?.__typename) throw new Error('__typename is missing in "isTagEdge"');
  return TagEdge_possibleTypes.includes(obj.__typename);
};

const Tag_possibleTypes: string[] = ["Tag"];
export const isTag = (obj?: { __typename?: any } | null): obj is Tag => {
  if (!obj?.__typename) throw new Error('__typename is missing in "isTag"');
  return Tag_possibleTypes.includes(obj.__typename);
};

const UserConnection_possibleTypes: string[] = ["UserConnection"];
export const isUserConnection = (
  obj?: { __typename?: any } | null,
): obj is UserConnection => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isUserConnection"');
  return UserConnection_possibleTypes.includes(obj.__typename);
};

const UserEdge_possibleTypes: string[] = ["UserEdge"];
export const isUserEdge = (
  obj?: { __typename?: any } | null,
): obj is UserEdge => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isUserEdge"');
  return UserEdge_possibleTypes.includes(obj.__typename);
};

const User_possibleTypes: string[] = ["User"];
export const isUser = (obj?: { __typename?: any } | null): obj is User => {
  if (!obj?.__typename) throw new Error('__typename is missing in "isUser"');
  return User_possibleTypes.includes(obj.__typename);
};

const AssetConnection_possibleTypes: string[] = ["AssetConnection"];
export const isAssetConnection = (
  obj?: { __typename?: any } | null,
): obj is AssetConnection => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isAssetConnection"');
  return AssetConnection_possibleTypes.includes(obj.__typename);
};

const AssetEdge_possibleTypes: string[] = ["AssetEdge"];
export const isAssetEdge = (
  obj?: { __typename?: any } | null,
): obj is AssetEdge => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isAssetEdge"');
  return AssetEdge_possibleTypes.includes(obj.__typename);
};

const Asset_possibleTypes: string[] = ["Asset"];
export const isAsset = (obj?: { __typename?: any } | null): obj is Asset => {
  if (!obj?.__typename) throw new Error('__typename is missing in "isAsset"');
  return Asset_possibleTypes.includes(obj.__typename);
};

const AssignedStage_possibleTypes: string[] = ["AssignedStage"];
export const isAssignedStage = (
  obj?: { __typename?: any } | null,
): obj is AssignedStage => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isAssignedStage"');
  return AssignedStage_possibleTypes.includes(obj.__typename);
};

const AssetUsage_possibleTypes: string[] = ["AssetUsage"];
export const isAssetUsage = (
  obj?: { __typename?: any } | null,
): obj is AssetUsage => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isAssetUsage"');
  return AssetUsage_possibleTypes.includes(obj.__typename);
};

const StageConnection_possibleTypes: string[] = ["StageConnection"];
export const isStageConnection = (
  obj?: { __typename?: any } | null,
): obj is StageConnection => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isStageConnection"');
  return StageConnection_possibleTypes.includes(obj.__typename);
};

const StageEdge_possibleTypes: string[] = ["StageEdge"];
export const isStageEdge = (
  obj?: { __typename?: any } | null,
): obj is StageEdge => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isStageEdge"');
  return StageEdge_possibleTypes.includes(obj.__typename);
};

const Stage_possibleTypes: string[] = ["Stage"];
export const isStage = (obj?: { __typename?: any } | null): obj is Stage => {
  if (!obj?.__typename) throw new Error('__typename is missing in "isStage"');
  return Stage_possibleTypes.includes(obj.__typename);
};

const StageAttributes_possibleTypes: string[] = ["StageAttributes"];
export const isStageAttributes = (
  obj?: { __typename?: any } | null,
): obj is StageAttributes => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isStageAttributes"');
  return StageAttributes_possibleTypes.includes(obj.__typename);
};

const AdminPlayerConnection_possibleTypes: string[] = ["AdminPlayerConnection"];
export const isAdminPlayerConnection = (
  obj?: { __typename?: any } | null,
): obj is AdminPlayerConnection => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isAdminPlayerConnection"');
  return AdminPlayerConnection_possibleTypes.includes(obj.__typename);
};

const AdminPlayerEdge_possibleTypes: string[] = ["AdminPlayerEdge"];
export const isAdminPlayerEdge = (
  obj?: { __typename?: any } | null,
): obj is AdminPlayerEdge => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isAdminPlayerEdge"');
  return AdminPlayerEdge_possibleTypes.includes(obj.__typename);
};

const AdminPlayer_possibleTypes: string[] = ["AdminPlayer"];
export const isAdminPlayer = (
  obj?: { __typename?: any } | null,
): obj is AdminPlayer => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isAdminPlayer"');
  return AdminPlayer_possibleTypes.includes(obj.__typename);
};

const Notification_possibleTypes: string[] = ["Notification"];
export const isNotification = (
  obj?: { __typename?: any } | null,
): obj is Notification => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isNotification"');
  return Notification_possibleTypes.includes(obj.__typename);
};

const Voice_possibleTypes: string[] = ["Voice"];
export const isVoice = (obj?: { __typename?: any } | null): obj is Voice => {
  if (!obj?.__typename) throw new Error('__typename is missing in "isVoice"');
  return Voice_possibleTypes.includes(obj.__typename);
};

const VoiceOutput_possibleTypes: string[] = ["VoiceOutput"];
export const isVoiceOutput = (
  obj?: { __typename?: any } | null,
): obj is VoiceOutput => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isVoiceOutput"');
  return VoiceOutput_possibleTypes.includes(obj.__typename);
};

const Mutation_possibleTypes: string[] = ["Mutation"];
export const isMutation = (
  obj?: { __typename?: any } | null,
): obj is Mutation => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isMutation"');
  return Mutation_possibleTypes.includes(obj.__typename);
};

const CalcSizes_possibleTypes: string[] = ["CalcSizes"];
export const isCalcSizes = (
  obj?: { __typename?: any } | null,
): obj is CalcSizes => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isCalcSizes"');
  return CalcSizes_possibleTypes.includes(obj.__typename);
};

const DeleteMedia_possibleTypes: string[] = ["DeleteMedia"];
export const isDeleteMedia = (
  obj?: { __typename?: any } | null,
): obj is DeleteMedia => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isDeleteMedia"');
  return DeleteMedia_possibleTypes.includes(obj.__typename);
};

const UploadFile_possibleTypes: string[] = ["UploadFile"];
export const isUploadFile = (
  obj?: { __typename?: any } | null,
): obj is UploadFile => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isUploadFile"');
  return UploadFile_possibleTypes.includes(obj.__typename);
};

const SaveMedia_possibleTypes: string[] = ["SaveMedia"];
export const isSaveMedia = (
  obj?: { __typename?: any } | null,
): obj is SaveMedia => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isSaveMedia"');
  return SaveMedia_possibleTypes.includes(obj.__typename);
};

const AuthMutation_possibleTypes: string[] = ["AuthMutation"];
export const isAuthMutation = (
  obj?: { __typename?: any } | null,
): obj is AuthMutation => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isAuthMutation"');
  return AuthMutation_possibleTypes.includes(obj.__typename);
};

const RefreshMutation_possibleTypes: string[] = ["RefreshMutation"];
export const isRefreshMutation = (
  obj?: { __typename?: any } | null,
): obj is RefreshMutation => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isRefreshMutation"');
  return RefreshMutation_possibleTypes.includes(obj.__typename);
};

const ConfirmPermission_possibleTypes: string[] = ["ConfirmPermission"];
export const isConfirmPermission = (
  obj?: { __typename?: any } | null,
): obj is ConfirmPermission => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isConfirmPermission"');
  return ConfirmPermission_possibleTypes.includes(obj.__typename);
};

const RequestPermission_possibleTypes: string[] = ["RequestPermission"];
export const isRequestPermission = (
  obj?: { __typename?: any } | null,
): obj is RequestPermission => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isRequestPermission"');
  return RequestPermission_possibleTypes.includes(obj.__typename);
};

const QuickAssignMutation_possibleTypes: string[] = ["QuickAssignMutation"];
export const isQuickAssignMutation = (
  obj?: { __typename?: any } | null,
): obj is QuickAssignMutation => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isQuickAssignMutation"');
  return QuickAssignMutation_possibleTypes.includes(obj.__typename);
};

const UpdateAttributeStatus_possibleTypes: string[] = ["UpdateAttributeStatus"];
export const isUpdateAttributeStatus = (
  obj?: { __typename?: any } | null,
): obj is UpdateAttributeStatus => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isUpdateAttributeStatus"');
  return UpdateAttributeStatus_possibleTypes.includes(obj.__typename);
};

const UpdateAttributeVisibility_possibleTypes: string[] = [
  "UpdateAttributeVisibility",
];
export const isUpdateAttributeVisibility = (
  obj?: { __typename?: any } | null,
): obj is UpdateAttributeVisibility => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isUpdateAttributeVisibility"');
  return UpdateAttributeVisibility_possibleTypes.includes(obj.__typename);
};

const UpdateUser_possibleTypes: string[] = ["UpdateUser"];
export const isUpdateUser = (
  obj?: { __typename?: any } | null,
): obj is UpdateUser => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isUpdateUser"');
  return UpdateUser_possibleTypes.includes(obj.__typename);
};

const DeleteUser_possibleTypes: string[] = ["DeleteUser"];
export const isDeleteUser = (
  obj?: { __typename?: any } | null,
): obj is DeleteUser => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isDeleteUser"');
  return DeleteUser_possibleTypes.includes(obj.__typename);
};

const BatchUserCreation_possibleTypes: string[] = ["BatchUserCreation"];
export const isBatchUserCreation = (
  obj?: { __typename?: any } | null,
): obj is BatchUserCreation => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isBatchUserCreation"');
  return BatchUserCreation_possibleTypes.includes(obj.__typename);
};

const SendEmail_possibleTypes: string[] = ["SendEmail"];
export const isSendEmail = (
  obj?: { __typename?: any } | null,
): obj is SendEmail => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isSendEmail"');
  return SendEmail_possibleTypes.includes(obj.__typename);
};

const ChangePassword_possibleTypes: string[] = ["ChangePassword"];
export const isChangePassword = (
  obj?: { __typename?: any } | null,
): obj is ChangePassword => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isChangePassword"');
  return ChangePassword_possibleTypes.includes(obj.__typename);
};

export const enumAssetTypeSortEnum = {
  ID_ASC: "ID_ASC" as const,
  ID_DESC: "ID_DESC" as const,
  NAME_ASC: "NAME_ASC" as const,
  NAME_DESC: "NAME_DESC" as const,
  DESCRIPTION_ASC: "DESCRIPTION_ASC" as const,
  DESCRIPTION_DESC: "DESCRIPTION_DESC" as const,
  FILE_LOCATION_ASC: "FILE_LOCATION_ASC" as const,
  FILE_LOCATION_DESC: "FILE_LOCATION_DESC" as const,
  CREATED_ON_ASC: "CREATED_ON_ASC" as const,
  CREATED_ON_DESC: "CREATED_ON_DESC" as const,
};

export const enumTagSortEnum = {
  ID_ASC: "ID_ASC" as const,
  ID_DESC: "ID_DESC" as const,
  NAME_ASC: "NAME_ASC" as const,
  NAME_DESC: "NAME_DESC" as const,
  COLOR_ASC: "COLOR_ASC" as const,
  COLOR_DESC: "COLOR_DESC" as const,
  CREATED_ON_ASC: "CREATED_ON_ASC" as const,
  CREATED_ON_DESC: "CREATED_ON_DESC" as const,
};

export const enumUserSortEnum = {
  ID_ASC: "ID_ASC" as const,
  ID_DESC: "ID_DESC" as const,
  USERNAME_ASC: "USERNAME_ASC" as const,
  USERNAME_DESC: "USERNAME_DESC" as const,
  PASSWORD_ASC: "PASSWORD_ASC" as const,
  PASSWORD_DESC: "PASSWORD_DESC" as const,
  EMAIL_ASC: "EMAIL_ASC" as const,
  EMAIL_DESC: "EMAIL_DESC" as const,
  BIN_NAME_ASC: "BIN_NAME_ASC" as const,
  BIN_NAME_DESC: "BIN_NAME_DESC" as const,
  ROLE_ASC: "ROLE_ASC" as const,
  ROLE_DESC: "ROLE_DESC" as const,
  FIRST_NAME_ASC: "FIRST_NAME_ASC" as const,
  FIRST_NAME_DESC: "FIRST_NAME_DESC" as const,
  LAST_NAME_ASC: "LAST_NAME_ASC" as const,
  LAST_NAME_DESC: "LAST_NAME_DESC" as const,
  DISPLAY_NAME_ASC: "DISPLAY_NAME_ASC" as const,
  DISPLAY_NAME_DESC: "DISPLAY_NAME_DESC" as const,
  ACTIVE_ASC: "ACTIVE_ASC" as const,
  ACTIVE_DESC: "ACTIVE_DESC" as const,
  CREATED_ON_ASC: "CREATED_ON_ASC" as const,
  CREATED_ON_DESC: "CREATED_ON_DESC" as const,
  FIREBASE_PUSHNOT_ID_ASC: "FIREBASE_PUSHNOT_ID_ASC" as const,
  FIREBASE_PUSHNOT_ID_DESC: "FIREBASE_PUSHNOT_ID_DESC" as const,
  DEACTIVATED_ON_ASC: "DEACTIVATED_ON_ASC" as const,
  DEACTIVATED_ON_DESC: "DEACTIVATED_ON_DESC" as const,
  UPLOAD_LIMIT_ASC: "UPLOAD_LIMIT_ASC" as const,
  UPLOAD_LIMIT_DESC: "UPLOAD_LIMIT_DESC" as const,
  INTRO_ASC: "INTRO_ASC" as const,
  INTRO_DESC: "INTRO_DESC" as const,
  CAN_SEND_EMAIL_ASC: "CAN_SEND_EMAIL_ASC" as const,
  CAN_SEND_EMAIL_DESC: "CAN_SEND_EMAIL_DESC" as const,
  LAST_LOGIN_ASC: "LAST_LOGIN_ASC" as const,
  LAST_LOGIN_DESC: "LAST_LOGIN_DESC" as const,
};

export const enumPrevilege = {
  NONE: "NONE" as const,
  OWNER: "OWNER" as const,
  APPROVED: "APPROVED" as const,
  PENDING_APPROVAL: "PENDING_APPROVAL" as const,
  REQUIRE_APPROVAL: "REQUIRE_APPROVAL" as const,
};

export const enumAssetSortEnum = {
  ID_ASC: "ID_ASC" as const,
  ID_DESC: "ID_DESC" as const,
  NAME_ASC: "NAME_ASC" as const,
  NAME_DESC: "NAME_DESC" as const,
  ASSET_TYPE_ID_ASC: "ASSET_TYPE_ID_ASC" as const,
  ASSET_TYPE_ID_DESC: "ASSET_TYPE_ID_DESC" as const,
  OWNER_ID_ASC: "OWNER_ID_ASC" as const,
  OWNER_ID_DESC: "OWNER_ID_DESC" as const,
  DESCRIPTION_ASC: "DESCRIPTION_ASC" as const,
  DESCRIPTION_DESC: "DESCRIPTION_DESC" as const,
  FILE_LOCATION_ASC: "FILE_LOCATION_ASC" as const,
  FILE_LOCATION_DESC: "FILE_LOCATION_DESC" as const,
  CREATED_ON_ASC: "CREATED_ON_ASC" as const,
  CREATED_ON_DESC: "CREATED_ON_DESC" as const,
  UPDATED_ON_ASC: "UPDATED_ON_ASC" as const,
  UPDATED_ON_DESC: "UPDATED_ON_DESC" as const,
  SIZE_ASC: "SIZE_ASC" as const,
  SIZE_DESC: "SIZE_DESC" as const,
  COPYRIGHT_LEVEL_ASC: "COPYRIGHT_LEVEL_ASC" as const,
  COPYRIGHT_LEVEL_DESC: "COPYRIGHT_LEVEL_DESC" as const,
};

export const enumStageSortEnum = {
  ID_ASC: "ID_ASC" as const,
  ID_DESC: "ID_DESC" as const,
  NAME_ASC: "NAME_ASC" as const,
  NAME_DESC: "NAME_DESC" as const,
  DESCRIPTION_ASC: "DESCRIPTION_ASC" as const,
  DESCRIPTION_DESC: "DESCRIPTION_DESC" as const,
  OWNER_ID_ASC: "OWNER_ID_ASC" as const,
  OWNER_ID_DESC: "OWNER_ID_DESC" as const,
  FILE_LOCATION_ASC: "FILE_LOCATION_ASC" as const,
  FILE_LOCATION_DESC: "FILE_LOCATION_DESC" as const,
  CREATED_ON_ASC: "CREATED_ON_ASC" as const,
  CREATED_ON_DESC: "CREATED_ON_DESC" as const,
  LAST_ACCESS_ASC: "LAST_ACCESS_ASC" as const,
  LAST_ACCESS_DESC: "LAST_ACCESS_DESC" as const,
};

export const enumAdminPlayerSortEnum = {
  ID_ASC: "ID_ASC" as const,
  ID_DESC: "ID_DESC" as const,
  USERNAME_ASC: "USERNAME_ASC" as const,
  USERNAME_DESC: "USERNAME_DESC" as const,
  PASSWORD_ASC: "PASSWORD_ASC" as const,
  PASSWORD_DESC: "PASSWORD_DESC" as const,
  EMAIL_ASC: "EMAIL_ASC" as const,
  EMAIL_DESC: "EMAIL_DESC" as const,
  BIN_NAME_ASC: "BIN_NAME_ASC" as const,
  BIN_NAME_DESC: "BIN_NAME_DESC" as const,
  ROLE_ASC: "ROLE_ASC" as const,
  ROLE_DESC: "ROLE_DESC" as const,
  FIRST_NAME_ASC: "FIRST_NAME_ASC" as const,
  FIRST_NAME_DESC: "FIRST_NAME_DESC" as const,
  LAST_NAME_ASC: "LAST_NAME_ASC" as const,
  LAST_NAME_DESC: "LAST_NAME_DESC" as const,
  DISPLAY_NAME_ASC: "DISPLAY_NAME_ASC" as const,
  DISPLAY_NAME_DESC: "DISPLAY_NAME_DESC" as const,
  ACTIVE_ASC: "ACTIVE_ASC" as const,
  ACTIVE_DESC: "ACTIVE_DESC" as const,
  CREATED_ON_ASC: "CREATED_ON_ASC" as const,
  CREATED_ON_DESC: "CREATED_ON_DESC" as const,
  FIREBASE_PUSHNOT_ID_ASC: "FIREBASE_PUSHNOT_ID_ASC" as const,
  FIREBASE_PUSHNOT_ID_DESC: "FIREBASE_PUSHNOT_ID_DESC" as const,
  DEACTIVATED_ON_ASC: "DEACTIVATED_ON_ASC" as const,
  DEACTIVATED_ON_DESC: "DEACTIVATED_ON_DESC" as const,
  UPLOAD_LIMIT_ASC: "UPLOAD_LIMIT_ASC" as const,
  UPLOAD_LIMIT_DESC: "UPLOAD_LIMIT_DESC" as const,
  INTRO_ASC: "INTRO_ASC" as const,
  INTRO_DESC: "INTRO_DESC" as const,
  CAN_SEND_EMAIL_ASC: "CAN_SEND_EMAIL_ASC" as const,
  CAN_SEND_EMAIL_DESC: "CAN_SEND_EMAIL_DESC" as const,
  LAST_LOGIN_ASC: "LAST_LOGIN_ASC" as const,
  LAST_LOGIN_DESC: "LAST_LOGIN_DESC" as const,
};

export const enumNotificationType = {
  MEDIA_USAGE: "MEDIA_USAGE" as const,
};
