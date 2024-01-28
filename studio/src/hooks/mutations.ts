import { message } from "ant-design-vue";
import { UpdateUserInput, User } from "genql/studio";
import { studioClient } from "services/graphql";
import { ref } from "vue";

export function useLoading<T extends unknown[], U>(
  operation: (...params: T) => Promise<U>,
  messages?: {
    loading: string;
    success: (result: U) => string;
    error?: (exception: unknown) => string;
    seconds?: number;
  },
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

export function useUpdateUser(messages?: Parameters<typeof useLoading>[1]) {
  return useLoading((user: User) => {
    const {
      username,
      password,
      email,
      binName,
      role,
      firstName,
      lastName,
      displayName,
      active,
      uploadLimit,
      intro,
      id,
    } = user;
    const inbound: UpdateUserInput = {
      username,
      password,
      email,
      binName,
      role,
      firstName,
      lastName,
      displayName,
      active,
      uploadLimit,
      intro,
      id,
    };
    return studioClient.mutation({
      updateUser: {
        __args: {
          inbound,
        },
        user: {
          __scalar: true,
        },
      },
    });
  }, messages);
}
