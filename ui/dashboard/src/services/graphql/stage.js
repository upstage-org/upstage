import { gql } from "graphql-request";
import { createClient } from "./graphql";

const client = createClient('stage_graphql')

export const stageFragment = gql`
  fragment stageFragment on Stage {
    id
    name
    fileLocation
    description
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
  }
`

export const assetFragment = gql`
  fragment assetFragment on Asset {
    id
    name
    assetType {
      id
      name
    }
    fileLocation
    dbId
  }
`

export default {
  createStage: (variables) => client.request(gql`
    mutation CreateStage($name: String, $description: String, $ownerId: String, $fileLocation: String) {
      createStage(input: {name: $name, description: $description, ownerId: $ownerId, fileLocation: $fileLocation}) {
        stage {
          id
          name
        }
      }
    }
  `, variables),
  updateStage: (variables) => client.request(gql`
    mutation UpdateStage($id: ID!, $name: String, $description: String, $ownerId: String, $fileLocation: String, $status: String) {
      updateStage(input: {id: $id, name: $name, description: $description, ownerId: $ownerId, fileLocation: $fileLocation, status: $status}) {
        stage {
          ...stageFragment
        }
      }
    }
    ${stageFragment}
  `, variables),
  stageList: (variables) => client.request(gql`
    query ListStage($id: ID, $nameLike: String) {
      stageList(id: $id, nameLike: $nameLike) {
        edges {
          node {
            ...stageFragment
          }
        }
      }
    }
    ${stageFragment}
  `, variables),
  uploadMedia: (variables) => client.request(gql`
    mutation uploadMedia($name: String!, $base64: String!, $mediaType: String) {
      uploadMedia(name: $name, base64: $base64, mediaType: $mediaType) {
        asset {
          id
        }
      }
    }
  `, variables),
  mediaList: (variables) => client.request(gql`
    query AssetList($id: ID, $nameLike: String, $assetTypeId: ID) {
      assetList(id: $id, nameLike: $nameLike, assetTypeId: $assetTypeId) {
        edges {
          node {
            ...assetFragment
          }
        }
      }
    }
    ${assetFragment}
  `, variables),
  assetTypeList: (variables) => client.request(gql`
    query AssetTypeList($id: ID, $nameLike: String) {
      assetTypeList(id: $id, nameLike: $nameLike) {
        edges {
          node {
            id
            dbId
            name
          }
        }
      }
    }
  `, variables),
}