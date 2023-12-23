import { useMutation } from "@vue/apollo-composable";
import { message } from "ant-design-vue";
import gql from "graphql-tag";
import { adminPlayerFragment } from "models/fragment";
import { User } from "models/studio";
import { ref } from "vue";

export function useLoading<T extends unknown[], U>(
  operation: (...params: T) => Promise<U>,
  messages?: {
    loading: string;
    success: (result: U) => string;
    error?: (exception: unknown) => string;
    seconds?: number;
  }
) {
  const key = +new Date();
  const loading = ref(false);

  return {
    loading,
    proceed: async (...params: Parameters<typeof operation>) => {
      loading.value = true;
      if (messages) {
        message.loading({ content: messages.loading, key });
      }
      try {
        const result = await operation(...params);
        if (messages) {
          message.success({
            content: messages.success(result),
            key,
            duration: messages.seconds,
          });
        }
        return result;
      } catch (error) {
        if (messages) {
          message.error({
            content: messages.error
              ? messages.error(error)
              : `Something went wrong, please try again later! (${error})`,
            key,
            duration: messages.seconds,
          });
        }
      } finally {
        loading.value = false;
      }
    },
  };
}

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
