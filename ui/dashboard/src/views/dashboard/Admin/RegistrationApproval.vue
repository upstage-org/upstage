<template>
  <DataTable :query="query" :headers="headers" numbered>
    <template #status="{ item }">
      <Switch
        v-model="item.active"
        @update:modelValue="toggleStatus(item)"
        className="is-rounded is-success"
        :loading="loadingUpdateUser"
      />
    </template>
  </DataTable>
</template>

<script>
import DataTable from "@/components/DataTable";
import Switch from "@/components/form/Switch";
import { userGraph } from "@/services/graphql";
import { displayName } from "@/utils/auth";
import { useMutation } from "@/services/graphql/composable";
import { notification } from "@/utils/notification";

export default {
  components: { DataTable, Switch },
  setup: () => {
    const query = userGraph.userList;
    const headers = [
      {
        title: "Username",
        key: "username",
      },
      {
        title: "Display Name",
        description: "Name displayed in chat",
        render: (item) => displayName(item),
      },
      {
        title: "Email",
        key: "email",
      },
      {
        title: "Registration Date",
        type: "date",
        key: "createdOn",
      },
      {
        title: "Role",
        render: (item) => (item.role > 0 ? "Admin" : "Player"),
      },
      {
        title: "Status",
        slot: "status",
      },
    ];

    const { mutation: updateUser, loading: loadingUpdateUser } = useMutation(
      userGraph.updateUser
    );
    const toggleStatus = async (user) => {
      const response = await updateUser(user);
      notification.success(
        response.updateUser.user.active
          ? `Account ${displayName(user)} activated successfully!`
          : `Account ${displayName(user)} deactivated successfully!`
      );
    };
    return { query, headers, toggleStatus, loadingUpdateUser };
  },
};
</script>

<style>
</style>