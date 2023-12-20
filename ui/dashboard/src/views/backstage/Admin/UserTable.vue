<template>
  <Dropdown
    :data="roles"
    :render-label="(item) => item.label"
    :render-value="(item) => item.value"
    v-model="filter.role"
  />
  <Field
    class="ml-2"
    style="display: inline-block; vertical-align: top"
    v-model="filter.keyword"
    right="fas fa-search"
    placeholder="Player name or email"
  />
  <Loading v-if="loading" />
  <DataTable v-show="!firstLoad" :data="users" :headers="headers" numbered :wrapper="false">
    <template #status="{ item }">
      <registration-approval :user="item" />
    </template>
    <template #role="{ item }">
      <switch-role :user="item" />
    </template>
    <template #upload-limit="{ item }">
      <upload-limit :user="item" :display-name="displayName(item)" />
    </template>
    <template #actions="{ item }">
      <div class="actions">
        <profile-management :item="item" :display-name="displayName(item)" :refresh="refresh" />
        <reset-password :user="item" :display-name="displayName(item)" />
        <delete-user :item="item" :display-name="displayName(item)" :refresh="refresh" />
      </div>
    </template>
  </DataTable>
</template>

<script>
import DataTable from "@/components/DataTable/index";
import Loading from "@/components/Loading";
import { userGraph } from "@/services/graphql";
import { displayName } from "@/utils/auth";
import RegistrationApproval from "./RegistrationApproval";
import ResetPassword from "./ResetPassword";
import SwitchRole from "./SwitchRole";
import UploadLimit from "./UploadLimit";
import ProfileManagement from "./ProfileManagement";
import DeleteUser from "./DeleteUser";
import Field from "@/components/form/Field.vue";
import Dropdown from "@/components/form/Dropdown.vue";
import { reactive, ref, watch, computed } from "vue";
import { includesIgnoreCase, titleCase } from "@/utils/common";
import { ROLES } from "@/utils/constants";
import { useQuery } from "@/services/graphql/composable";

export default {
  components: {
    DataTable,
    Loading,
    RegistrationApproval,
    ResetPassword,
    SwitchRole,
    UploadLimit,
    ProfileManagement,
    DeleteUser,
    Field,
    Dropdown,
  },
  props: ["actionColumn", "actionSort"],
  setup: () => {
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

    const filter = reactive({
      keyword: "",
      role: null,
    });
    const roles = [
      {
        label: "All roles",
        value: null,
      },
    ];
    for (let role in ROLES) {
      roles.push({
        label: titleCase(role),
        value: ROLES[role],
      });
    }
    const { nodes, refresh, loading } = useQuery(userGraph.userList);
    const users = computed(() => {
      let res = nodes.value;
      if (!res) {
        return [];
      }
      if (filter.keyword) {
        res = res.filter((item) =>
          includesIgnoreCase(
            `${item.firstName} ${item.lastName} ${item.username} ${item.email} ${item.displayName}`,
            filter.keyword.trim()
          )
        );
      }
      if (filter.role) {
        res = res.filter((item) => item.role === filter.role);
      }
      return res;
    });

    const firstLoad = ref(true);
    watch(loading, value => {
      if (!value) {
        firstLoad.value = false;
      }
    });

    return { headers, users, refresh, displayName, filter, roles, loading, firstLoad };
  },
};
</script>

<style scoped lang="scss">
.actions {
  display: flex;
  width: 120px;
}
</style>