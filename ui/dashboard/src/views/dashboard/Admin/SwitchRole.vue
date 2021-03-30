<template>
  <UserTable action-column="Change Password">
    <template #action="{ item }">
      <Confirm @confirm="(close) => saveRole(item, close)" :loading="loading">
        <template #render="{ confirm }">
          <Dropdown
            :data="roles"
            :render-label="(item) => item.label"
            :render-value="(item) => item.value"
            v-model="selectedRole"
            @update:model-value="confirm()"
          />
        </template>
      </Confirm>
    </template>
  </UserTable>
</template>

<script>
import UserTable from "./UserTable";
import { useMutation } from "@/services/graphql/composable";
import { userGraph } from "@/services/graphql";
import Dropdown from "@/components/form/Dropdown";
import Confirm from "@/components/Confirm";
import { ROLES } from "@/utils/constants";
import { titleCase } from "@/utils/common";
import { displayName, displayRole } from "@/utils/auth";
import { ref } from "@vue/reactivity";

export default {
  components: { UserTable, Dropdown, Confirm },
  setup: () => {
    const roles = [];
    for (let role in ROLES) {
      roles.push({
        label: titleCase(role),
        value: ROLES[role],
      });
    }
    const selectedRole = ref();
    const { save, loading } = useMutation(userGraph.updateUser);
    const saveRole = async (user, close) => {
      user.role = selectedRole.value;
      await save(
        `Successfully switch ${displayName(user)}'s role to ${displayRole(
          user
        )}!`,
        user
      );
      close();
    };
    return { roles, selectedRole, loading, saveRole };
  },
};
</script>

<style>
</style>