import { gql } from "graphql-request";
import { createClient } from "./graphql";

const client = createClient("user_graphql");

export const userFragment = gql`
  fragment userFragment on User {
    id
    dbId
    username
    firstName
    lastName
    displayName
    email
    active
    createdOn
    role
    uploadLimit
    intro
  }
`;

export default {
  createUser: (variables) =>
    client.request(
      gql`
        mutation CreateUser(
          $username: String!
          $password: String!
          $email: String
          $firstName: String
          $lastName: String
          $intro: String
          $token: String
        ) {
          createUser(
            inbound: {
              username: $username
              password: $password
              email: $email
              firstName: $firstName
              lastName: $lastName
              intro: $intro
              token: $token
            }
          ) {
            user {
              ...userFragment
            }
          }
        }
        ${userFragment}
      `,
      variables,
    ),
  updateUser: (variables) =>
    client.request(
      gql`
        mutation UpdateUser(
          $id: ID!
          $displayName: String
          $firstName: String
          $lastName: String
          $email: String
          $password: String
          $active: Boolean
          $role: Int
          $uploadLimit: Int
        ) {
          updateUser(
            inbound: {
              id: $id
              displayName: $displayName
              firstName: $firstName
              lastName: $lastName
              email: $email
              password: $password
              active: $active
              role: $role
              uploadLimit: $uploadLimit
            }
          ) {
            user {
              ...userFragment
            }
          }
        }
        ${userFragment}
      `,
      variables,
    ),
  refreshUser: (variables, headers) =>
    client.request(
      gql`
        mutation RefreshToken($refreshToken: String) {
          refreshUser(refreshToken: $refreshToken) {
            newToken
          }
        }
      `,
      variables,
      headers,
    ),
  currentUser: () =>
    client.request(gql`
      query {
        currentUser {
          ...userFragment
        }
      }
      ${userFragment}
    `),
  userList: () =>
    client.request(gql`
      query UserList($first: Int, $after: String) {
        userList(
          sort: USERNAME_ASC
          active: true
          first: $first
          after: $after
        ) {
          totalCount
          edges {
            node {
              ...userFragment
            }
          }
        }
      }
      ${userFragment}
    `),
  changePassword: (variables) =>
    client.request(
      gql`
        mutation ChangePassword(
          $id: ID!
          $oldPassword: String!
          $newPassword: String!
        ) {
          changePassword(
            inbound: {
              id: $id
              oldPassword: $oldPassword
              newPassword: $newPassword
            }
          ) {
            success
          }
        }
      `,
      variables,
    ),
  deleteUser: (variables) =>
    client.request(
      gql`
        mutation DeleteUser($id: ID!) {
          deleteUser(inbound: { id: $id }) {
            success
          }
        }
      `,
      variables,
    ),
  batchUserCreation: (variables) =>
    client.request(
      gql`
        mutation BatchUserCreation(
          $users: [BatchUserInput]!
          $stageIds: [Int]
        ) {
          batchUserCreation(users: $users, stageIds: $stageIds) {
            users {
              dbId
            }
          }
        }
      `,
      variables,
    ),
  requestPasswordReset: (variables) =>
    client.request(
      gql`
        mutation RequestPasswordReset($usernameOrEmail: String) {
          requestPasswordReset(usernameOrEmail: $usernameOrEmail) {
            message
            username
          }
        }
      `,
      variables,
    ),
  verifyPasswordReset: (variables) =>
    client.request(
      gql`
        mutation verifyPasswordReset($username: String, $otp: String) {
          verifyPasswordReset(username: $username, otp: $otp) {
            message
          }
        }
      `,
      variables,
    ),
  passwordReset: (variables) =>
    client.request(
      gql`
        mutation PasswordReset(
          $username: String
          $otp: String
          $password: String
        ) {
          passwordReset(username: $username, otp: $otp, password: $password) {
            message
          }
        }
      `,
      variables,
    ),
};
