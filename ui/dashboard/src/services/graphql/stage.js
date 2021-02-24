import { gql } from "graphql-request";
import { createClient } from "./graphql";

const client = createClient('stage_graphql')

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
  stageList: (variables) => client.request(gql`
    query ListStage($id: ID, $nameLike: String) {
      stageList(id: $id, nameLike: $nameLike) {
        edges {
          node {
            id
            name
            fileLocation
            owner {
              id
              username
              displayName
            }
          }
        }
      }
    }
  `, variables)
} 