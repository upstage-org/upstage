import configs from "config";
import { computed } from "vue";
import { useUpdateUser } from "../hooks/mutations";
import { studioClient } from "services/graphql";
import { useAsyncState } from "@vueuse/core";
import { User } from "genql/studio";

const { state, execute } = useAsyncState(
  () =>
    studioClient.query({
      whoami: {
        __scalar: true,
      },
    }),
  {
    whoami: null,
  },
  {
    resetOnExecute: false,
  },
);

export const whoami = computed(() => state.value.whoami);
export const refreshWhoami = () => execute(0);

const isAdmin = computed(() =>
  [configs.ROLES.ADMIN, configs.ROLES.SUPER_ADMIN].includes(
    whoami.value?.role ?? 0,
  ),
);

export function useWhoAmI() {
  return { whoami, isAdmin };
}

export function useUpdateProfile() {
  const { proceed, loading } = useUpdateUser({
    loading: "Saving your profile...",
    success: () => {
      refreshWhoami();
      return "Your profile information saved successfully!";
    },
  });
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
