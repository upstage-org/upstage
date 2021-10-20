import { gql } from "graphql-request";
import { createClient } from "./graphql";

const client = createClient('stage_graphql')

export const stageFragment = gql`
  fragment stageFragment on Stage {
    id
    name
    fileLocation
    description
    permission
    owner {
      id
      username
      displayName
    }
    attributes {
      id
      name
      description
    }
    media {
      id
      name
      type
      src
      description
    }
    dbId
  }
`

export const assetFragment = gql`
  fragment assetFragment on Asset {
    id
    name
    description
    assetType {
      id
      name
    }
    owner {
      id
      username
      displayName
    }
    createdOn
    src
    dbId
    copyrightLevel
    playerAccess
    permission
    sign
  }
`

export const sceneFragment = gql`
  fragment sceneFragment on Scene {
    id
    name
    payload
    scenePreview
  }
`

const studioGraph = {
  mediaList: (variables?: any) => client.request(gql`
    query AssetList($id: ID, $nameLike: String, $assetType: String) {
      assetList(id: $id, nameLike: $nameLike, assetType: $assetType, sort: ID_DESC) {
        edges {
          node {
            ...assetFragment
            stages {
              id
              name
              url
            }
          }
        }
      }
    }
    ${assetFragment}
  `, variables)
}

export default studioGraph