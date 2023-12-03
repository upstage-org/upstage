import { useQuery } from "@vue/apollo-composable";
import configs from "config";
import gql from "graphql-tag";
import { StudioGraph, User } from "models/studio";
import { computed } from "vue";
import { useUpdateUser } from "./mutations";
import { message } from "ant-design-vue";

const {
  result,
  loading: loadingCurrentUser,
  refetch,
} = useQuery<StudioGraph>(gql`
  query WhoAmI {
    whoami {
      id
      username
      firstName
      lastName
      displayName
      email
      role
      roleName
      uploadLimit
      active
      intro
    }
  }
`);

const whoami = computed(() => result.value?.whoami);

const isAdmin = computed(() =>
  [configs.ROLES.ADMIN, configs.ROLES.SUPER_ADMIN].includes(
    result.value?.whoami?.role ?? 0
  )
);

const { mutate: updateUser, loading: savingUser } = useUpdateUser();

const save = async (player: User) => {
  const res = await updateUser({
    ...player,
  });
  console.log({ res });
  try {
    if (result.value?.whoami && res?.data?.updateUser.user) {
      result.value.whoami = res.data.updateUser.user;
    }
  } catch {
    refetch();
  }
  message.success(`Successfully update your profile!`);
};

const loading = computed(() => loadingCurrentUser.value || savingUser.value);

export function useWhoAmI() {
  return { whoami, isAdmin, loadingCurrentUser };
}

export function useUpdateProfile() {
  return { whoami, loading, save };
}

export function useLogout() {
  return () => {
    localStorage.clear();
    window.location.href = "/";
  };
}
