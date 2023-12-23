// @ts-nocheck
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type Scalars = {
  ID: string;
  Int: number;
  String: string;
  Boolean: boolean;
};

export interface Query {
  node: Node | null;
  nginx: NginxConfig | null;
  system: SystemConfig | null;
  foyer: FoyerConfig | null;
  __typename: "Query";
}

/** An object with an ID */
export interface Node {
  /** The ID of the object. */
  id: Scalars["ID"];
  __typename: string;
}

export interface NginxConfig {
  uploadLimit: Scalars["Int"] | null;
  __typename: "NginxConfig";
}

export interface SystemConfig {
  termsOfService: Scalars["String"] | null;
  manual: Scalars["String"] | null;
  esp: Scalars["String"] | null;
  enableDonate: Scalars["Boolean"] | null;
  __typename: "SystemConfig";
}

export interface FoyerConfig {
  title: Scalars["String"] | null;
  description: Scalars["String"] | null;
  menu: Scalars["String"] | null;
  showRegistration: Scalars["Boolean"] | null;
  __typename: "FoyerConfig";
}

export interface Mutation {
  /** Mutation to update Terms of Service's URL. */
  updateTermsOfService: UpdateTermsOfService | null;
  /** Mutation to customise foyer. */
  saveConfig: SaveConfig | null;
  /** Mutation to customise foyer. */
  sendEmail: SendEmail | null;
  __typename: "Mutation";
}

/** Mutation to update Terms of Service's URL. */
export interface UpdateTermsOfService {
  /** The updated Terms of Service's URL. */
  url: Scalars["String"] | null;
  __typename: "UpdateTermsOfService";
}

/** Mutation to customise foyer. */
export interface SaveConfig {
  /** True if the config was saved. */
  success: Scalars["Boolean"] | null;
  __typename: "SaveConfig";
}

/** Mutation to customise foyer. */
export interface SendEmail {
  /** True if the config was saved. */
  success: Scalars["Boolean"] | null;
  __typename: "SendEmail";
}

export interface QueryGenqlSelection {
  node?: NodeGenqlSelection & {
    __args: {
      /** The ID of the object */
      id: Scalars["ID"];
    };
  };
  nginx?: NginxConfigGenqlSelection;
  system?: SystemConfigGenqlSelection;
  foyer?: FoyerConfigGenqlSelection;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

/** An object with an ID */
export interface NodeGenqlSelection {
  /** The ID of the object. */
  id?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

export interface NginxConfigGenqlSelection {
  uploadLimit?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

export interface SystemConfigGenqlSelection {
  termsOfService?: boolean | number;
  manual?: boolean | number;
  esp?: boolean | number;
  enableDonate?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

export interface FoyerConfigGenqlSelection {
  title?: boolean | number;
  description?: boolean | number;
  menu?: boolean | number;
  showRegistration?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

export interface MutationGenqlSelection {
  /** Mutation to update Terms of Service's URL. */
  updateTermsOfService?: UpdateTermsOfServiceGenqlSelection & {
    __args: { url: Scalars["String"] };
  };
  /** Mutation to customise foyer. */
  saveConfig?: SaveConfigGenqlSelection & {
    __args: {
      /** The name of the config. */
      name: Scalars["String"];
      /** The value of the config. */
      value: Scalars["String"];
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
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

/** Mutation to update Terms of Service's URL. */
export interface UpdateTermsOfServiceGenqlSelection {
  /** The updated Terms of Service's URL. */
  url?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

/** Mutation to customise foyer. */
export interface SaveConfigGenqlSelection {
  /** True if the config was saved. */
  success?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

/** Mutation to customise foyer. */
export interface SendEmailGenqlSelection {
  /** True if the config was saved. */
  success?: boolean | number;
  __typename?: boolean | number;
  __scalar?: boolean | number;
}

const Query_possibleTypes: string[] = ["Query"];
export const isQuery = (obj?: { __typename?: any } | null): obj is Query => {
  if (!obj?.__typename) throw new Error('__typename is missing in "isQuery"');
  return Query_possibleTypes.includes(obj.__typename);
};

const Node_possibleTypes: string[] = [];
export const isNode = (obj?: { __typename?: any } | null): obj is Node => {
  if (!obj?.__typename) throw new Error('__typename is missing in "isNode"');
  return Node_possibleTypes.includes(obj.__typename);
};

const NginxConfig_possibleTypes: string[] = ["NginxConfig"];
export const isNginxConfig = (
  obj?: { __typename?: any } | null,
): obj is NginxConfig => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isNginxConfig"');
  return NginxConfig_possibleTypes.includes(obj.__typename);
};

const SystemConfig_possibleTypes: string[] = ["SystemConfig"];
export const isSystemConfig = (
  obj?: { __typename?: any } | null,
): obj is SystemConfig => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isSystemConfig"');
  return SystemConfig_possibleTypes.includes(obj.__typename);
};

const FoyerConfig_possibleTypes: string[] = ["FoyerConfig"];
export const isFoyerConfig = (
  obj?: { __typename?: any } | null,
): obj is FoyerConfig => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isFoyerConfig"');
  return FoyerConfig_possibleTypes.includes(obj.__typename);
};

const Mutation_possibleTypes: string[] = ["Mutation"];
export const isMutation = (
  obj?: { __typename?: any } | null,
): obj is Mutation => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isMutation"');
  return Mutation_possibleTypes.includes(obj.__typename);
};

const UpdateTermsOfService_possibleTypes: string[] = ["UpdateTermsOfService"];
export const isUpdateTermsOfService = (
  obj?: { __typename?: any } | null,
): obj is UpdateTermsOfService => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isUpdateTermsOfService"');
  return UpdateTermsOfService_possibleTypes.includes(obj.__typename);
};

const SaveConfig_possibleTypes: string[] = ["SaveConfig"];
export const isSaveConfig = (
  obj?: { __typename?: any } | null,
): obj is SaveConfig => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isSaveConfig"');
  return SaveConfig_possibleTypes.includes(obj.__typename);
};

const SendEmail_possibleTypes: string[] = ["SendEmail"];
export const isSendEmail = (
  obj?: { __typename?: any } | null,
): obj is SendEmail => {
  if (!obj?.__typename)
    throw new Error('__typename is missing in "isSendEmail"');
  return SendEmail_possibleTypes.includes(obj.__typename);
};
