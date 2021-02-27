import { gql } from "graphql-request";
import { createClient } from "./graphql";

const client = createClient('user_graphql')

export default {
  createUser: (variables) => client.request(gql`
    mutation CreateUser($username: String!, $password: String!, $email: String, $firstName: String, $lastName: String) {
      createUser(input: {username: $username, password: $password, email: $email, firstName: $firstName, lastName: $lastName, active: true}) {
        user {
          id
          username
        }
      }
    }
  `, variables),
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
  `),
  refreshUser: (variables, headers) => client.request(gql`
    mutation RefreshToken($refreshToken: String) {
      refreshUser(refreshToken: $refreshToken) {
        newToken
      }
    }
  `, variables, headers),
  loggedIn: () => client.request(gql`
    query {
      loggedIn {
        edges {
          node {
            id
            dbId
            username
            displayName
            firstName
            lastName
            email
            phone
            active
          }
        }
      } 
    }
  `),
} 