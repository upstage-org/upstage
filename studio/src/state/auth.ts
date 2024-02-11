import configs from "config";
import { computed } from "vue";
import { useLoading, useUpdateUser } from "../hooks/mutations";
import { message } from "ant-design-vue";
import { studioClient } from "services/graphql";
import { useAsyncState } from "@vueuse/core";
import { User } from "genql/studio";

const { state } = useAsyncState(
  studioClient.query({
    whoami: {
      __scalar: true,
    },
  }),
  {
    whoami: null,
  }
);

const whoami = computed(() => state.value.whoami);

const isAdmin = computed(() =>
  [configs.ROLES.ADMIN, configs.ROLES.SUPER_ADMIN].includes(
    whoami.value?.role ?? 0
  )
);

export function useWhoAmI() {
  return { whoami, isAdmin };
}

export async function useUpdateProfile(
  messages?: Parameters<typeof useLoading>[1]
) {
  const { proceed, loading } = useUpdateUser(messages);
  return {
    whoami,
    updateProfile: async (player: User) => {
      const res = await proceed({
        ...player,
      });
      return res;
    },
    loading,
  };
}

export function useLogout() {
  return () => {
    localStorage.clear();
    window.location.href = "/";
  };
}
