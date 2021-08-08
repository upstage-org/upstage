<template>
  <DataTable :query="query" :headers="headers" numbered>
    <template #status="{ item }">
      <registration-approval :user="item" />
    </template>
    <template #role="{ item }">
      <switch-role :user="item" />
    </template>
    <template #upload-limit="{ item }">
      <upload-limit :user="item" :display-name="displayName(item)" />
    </template>
    <template #actions="{ item, refresh }">
      <div class="actions">
        <profile-management
          :item="item"
          :display-name="displayName(item)"
          :refresh="refresh"
        />
        <reset-password :user="item" :display-name="displayName(item)" />
        <delete-user
          :item="item"
          :display-name="displayName(item)"
          :refresh="refresh"
        />
      </div>
    </template>
  </DataTable>
</template>

<script>
import DataTable from "@/components/DataTable/index";
import { userGraph } from "@/services/graphql";
import { displayName } from "@/utils/auth";
import RegistrationApproval from "./RegistrationApproval";
import ResetPassword from "./ResetPassword";
import SwitchRole from "./SwitchRole";
import UploadLimit from "./UploadLimit";
import ProfileManagement from "./ProfileManagement";
import DeleteUser from "./DeleteUser";

export default {
  components: {
    DataTable,
    RegistrationApproval,
    ResetPassword,
    SwitchRole,
    UploadLimit,
    ProfileManagement,
    DeleteUser,
  },
  props: ["actionColumn", "actionSort"],
  setup: () => {
    const query = userGraph.userList;
    const headers = [
      {
        title: "Username",
        key: "username",
        sortable: true,
      },
      {
        title: "Display Name",
        render: (item) => displayName(item),
        sortable: true,
      },
      {
        title: "Email",
        key: "email",
        sortable: true,
      },
      {
        title: "Date Registered",
        key: "createdOn",
        type: "date",
        sortable: true,
        defaultSortOrder: false,
      },
      {
        title: "Role",
        slot: "role",
        align: "center",
      },
      {
        title: "Status",
        slot: "status",
        align: "center",
        sortable: (a, b) => b.active - a.active,
      },
      {
        title: "Upload Limit",
        slot: "upload-limit",
        align: "center",
      },
      {
        title: "",
        slot: "actions",
        align: "center",
      },
    ];
    return { query, headers, displayName };
  },
};
</script>

<style scoped lang="scss">
.actions {
  display: flex;
  width: 120px;
}
</style>