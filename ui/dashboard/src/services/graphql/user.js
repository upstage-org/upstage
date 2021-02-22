import { gql } from "graphql-request";
import { createClient } from "./graphql";

const client = createClient('user_graphql')

export default {
  updateUser: (variables) => client.request(gql`
    mutation UpdateUser($id: ID!, $displayName: String) {
      updateUser(input: {id: $id, displayName: $displayName}) {
        user {
          id
          username
          displayName
        }
      }
    }
  `, variables),
  oneUser: () => client.request(gql`
    {
      oneUser {
        edges {
          node {
            id
            username
            displayName
          }
        }
      }
    }
  `)
} 