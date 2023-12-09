import configs from "config";
import { User } from "models/studio";
import { computed, ref } from "vue";
import { useUpdateUser } from "./mutations";
import { message } from "ant-design-vue";
import graphqlClient from "services/graphql";

const currentUserState = ref(
  await graphqlClient.query({
    whoami: {
      __scalar: true,
    },
  }),
);

const whoami = computed(() => currentUserState.value.whoami);

const isAdmin = computed(() =>
  [configs.ROLES.ADMIN, configs.ROLES.SUPER_ADMIN].includes(
    whoami.value?.role ?? 0,
  ),
);

const { mutate: updateUser, loading: savingUser } = useUpdateUser();

const save = async (player: User) => {
  const res = await updateUser({
    ...player,
  });
  message.success(`Successfully update your profile!`);
};

export async function useWhoAmI() {
  return { whoami, isAdmin };
}

export async function useUpdateProfile() {
  return { whoami, save };
}

export function useLogout() {
  return () => {
    localStorage.clear();
    window.location.href = "/";
  };
}
