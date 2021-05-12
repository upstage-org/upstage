<template>
  <UserTable
    action-column="Status"
    :action-sort="(a, b) => b.active - a.active"
  >
    <template #action="{ item }">
      <Switch
        v-model="item.active"
        @update:modelValue="toggleStatus(item)"
        className="is-rounded is-success"
        :loading="item.loading"
      />
    </template>
  </UserTable>
</template>

<script>
import UserTable from "./UserTable";
import Switch from "@/components/form/Switch";
import { userGraph } from "@/services/graphql";
import { displayName } from "@/utils/auth";
import { useMutation } from "@/services/graphql/composable";
import { notification } from "@/utils/notification";

export default {
  components: { UserTable, Switch },
  setup: () => {
    const { mutation: updateUser } = useMutation(userGraph.updateUser);
    const toggleStatus = async (user) => {
      user.loading = true;
      const response = await updateUser(user);
      notification.success(
        response.updateUser.user.active
          ? `Account ${displayName(user)} activated successfully!`
          : `Account ${displayName(user)} deactivated successfully!`
      );
      user.loading = false;
    };
    return { toggleStatus };
  },
};
</script>

<style>
</style>