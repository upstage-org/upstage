import configs from "config";
import { User } from "models/studio";
import { computed, ref } from "vue";
import { useUpdateUser } from "./mutations";
import { message } from "ant-design-vue";
import { studioClient } from "services/graphql";
import { useAsyncState } from "@vueuse/core";

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

const { mutate: updateUser, loading: savingUser } = useUpdateUser();

export function useWhoAmI() {
  return { whoami, isAdmin };
}

export async function useUpdateProfile() {
  return {
    whoami,
    updateProfile: async (player: User) => {
      const res = await updateUser({
        ...player,
      });
      message.success(`Successfully update your profile!`);
      return res;
    },
  };
}

export function useLogout() {
  return () => {
    localStorage.clear();
    window.location.href = "/";
  };
}
