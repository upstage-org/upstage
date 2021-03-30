<template>
  <DataTable :query="query" :headers="headers" numbered>
    <template #action="{ item }">
      <slot name="action" :item="item" :display-name="displayName(item)" />
    </template>
  </DataTable>
</template>

<script>
import DataTable from "@/components/DataTable/index";
import { userGraph } from "@/services/graphql";
import { displayName } from "@/utils/auth";

export default {
  components: { DataTable },
  props: ["actionColumn"],
  setup: (props) => {
    const query = userGraph.userList;
    const headers = [
      {
        title: "Username",
        key: "username",
        sortable: true,
      },
      {
        title: "Display Name",
        description: "Name displayed in chat",
        render: (item) => displayName(item),
        sortable: true,
      },
      {
        title: "Email",
        key: "email",
        sortable: true,
      },
      {
        title: "Role",
        render: (item) => (item.role > 0 ? "Admin" : "Player"),
        sortable: true,
      },
      {
        title: "Date Registered",
        key: "createdOn",
        type: "date",
        sortable: true,
      },
      {
        title: props.actionColumn,
        slot: "action",
        align: "center",
      },
    ];
    return { query, headers, displayName };
  },
};
</script>

<style>
</style>