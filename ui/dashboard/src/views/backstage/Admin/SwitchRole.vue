<template>
  <Confirm @confirm="(close) => saveRole(item, close)" :loading="loading">
    <template #render="{ confirm }">
      <Dropdown
        :data="roles"
        :render-label="(item) => item.label"
        :render-value="(item) => item.value"
        :model-value="item.selectedRole ?? item.role"
        :isUp="item.lastItem"
        @update:model-value="
          item.selectedRole = $event;
          confirm();
        "
      />
    </template>
  </Confirm>
</template>

<script>
import { useMutation } from "@/services/graphql/composable";
import { userGraph } from "@/services/graphql";
import Dropdown from "@/components/form/Dropdown";
import Confirm from "@/components/Confirm";
import { ROLES } from "@/utils/constants";
import { titleCase } from "@/utils/common";
import { displayName, displayRole } from "@/utils/auth";

export default {
  components: { Dropdown, Confirm },
  props: ["user"],
  setup: (props) => {
    const roles = [];
    for (let role in ROLES) {
      roles.push({
        label: titleCase(role),
        value: ROLES[role],
      });
    }
    const { save, loading } = useMutation(userGraph.updateUser);
    const saveRole = async (user, close) => {
      user.role = user.selectedRole;
      await save(
        `Successfully switch ${displayName(user)}'s role to ${displayRole(
          user
        )}!`,
        user
      );
      close();
    };
    return { roles, loading, saveRole, item: props.user };
  },
};
</script>

<style>
</style>