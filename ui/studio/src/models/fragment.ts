import gql from "graphql-tag";

export const permissionFragment = gql`
  fragment permissionFragment on AssetUsage {
    id
    userId
    assetId
    approved
    seen
    createdOn
    note
    user {
      username
      displayName
    }
  }
`;