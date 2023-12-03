import { useMutation } from "@vue/apollo-composable";
import gql from "graphql-tag";
import { adminPlayerFragment } from "models/fragment";
import { User } from "models/studio";

export function useUpdateUser() {
  return useMutation<
    {
      updateUser: {
        user: User;
      };
    },
    {
      id: string;
      displayName?: string;
      firstName?: string;
      lastName?: string;
      email?: string;
      password?: string;
      active?: boolean;
      role?: number;
      uploadLimit?: number;
    }
  >(gql`
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
      $intro: String
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
          intro: $intro
        }
      ) {
        user {
          ...adminPlayerFragment
        }
      }
    }
    ${adminPlayerFragment}
  `);
}
