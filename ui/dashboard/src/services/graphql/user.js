import { gql } from "graphql-request";
import { createClient } from "./graphql";

const client = createClient('user_graphql')

export const userFragment = gql`
  fragment userFragment on User {
    id
    username
    firstName
    lastName
    displayName
    email
    phone
    active
    createdOn
    agreedToTerms
    okToSms
    validatedViaPortal
  }
`

export default {
  createUser: (variables) => client.request(gql`
    mutation CreateUser($username: String!, $password: String!, $email: String, $firstName: String, $lastName: String) {
      createUser(input: {username: $username, password: $password, email: $email, firstName: $firstName, lastName: $lastName, active: true}) {
        user {
          ...userFragment
        }
      }
    }
    ${userFragment}
  `, variables),
  updateUser: (variables) => client.request(gql`
    mutation UpdateUser($id: ID!, $displayName: String, $firstName: String, $lastName: String, $email: String, $phone: String, $agreedToTerms: Boolean, $okToSms: Boolean, $validatedViaPortal: Boolean) {
      updateUser(input: {id: $id, displayName: $displayName, firstName: $firstName, lastName: $lastName, email: $email, phone: $phone, agreedToTerms: $agreedToTerms, okToSms: $okToSms, validatedViaPortal: $validatedViaPortal}) {
        user {
          ...userFragment
        }
      }
    }
    ${userFragment}
  `, variables),
  saveNickname: (variables) => client.request(gql`
    mutation UpdateUser($id: ID!, $displayName: String) {
      updateUser(input: {id: $id, displayName: $displayName}) {
        user {
          ...userFragment
        }
      }
    }
    ${userFragment}
  `, variables),
  refreshUser: (variables, headers) => client.request(gql`
    mutation RefreshToken($refreshToken: String) {
      refreshUser(refreshToken: $refreshToken) {
        newToken
      }
    }
  `, variables, headers),
  currentUser: () => client.request(gql`
    query {
      currentUser {
        ...userFragment
      } 
    }
    ${userFragment}
  `),
} 