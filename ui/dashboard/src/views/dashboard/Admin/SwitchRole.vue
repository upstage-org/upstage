<template>
  <UserTable action-column="Change Password">
    <template #action="{ item }">
      <Dropdown
        :data="roles"
        :render-label="(item) => item.label"
        :render-value="(item) => item.value"
        v-model="item.role"
      />
    </template>
  </UserTable>
</template>

<script>
import UserTable from "./UserTable";
import { ref } from "@vue/reactivity";
import { useMutation } from "@/services/graphql/composable";
import { userGraph } from "@/services/graphql";
import Dropdown from "@/components/form/Dropdown";
import { ROLES } from "@/utils/constants";
import { titleCase } from "@/utils/common";

export default {
  components: { UserTable, Dropdown },
  setup: () => {
    const password = ref("pleasechange");
    const roles = [];
    for (let role in ROLES) {
      roles.push({
        label: titleCase(role),
        value: ROLES[role],
      });
    }
    const { save, loading } = useMutation(userGraph.updateUser);
    const savePassword = async (user, displayName, closeModal) => {
      user.password = password.value;
      await save(`Successfully reset ${displayName} password!`, user);
      closeModal();
    };
    return { password, roles, loading, savePassword };
  },
};
</script>

<style>
</style>