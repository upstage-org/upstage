<template>
  <DataTable :query="stageGraph.stageList" :headers="headers">
    <template #name="{ item }">
      <router-link to="/live" class="has-text-primary has-text-weight-bold">
        {{ item.name }}
      </router-link>
    </template>
    <template #detail="{ item }">
      <Modal>
        <template #trigger>
          <i class="fas fa-lg fa-eye" />
        </template>
        <template #header>Stage Detail</template>
        <template #content><Detail :name="item.name" /></template>
        <template #footer><ActionButtons :stage="item" /></template>
      </Modal>
    </template>
    <template #edit="{ item }">
      <router-link :to="`/dashboard/stage-management/${item.id}/`">
        <i class="fa fa-lg fa-pen has-text-black"></i>
      </router-link>
    </template>
  </DataTable>
</template>

<script setup>
import { useQuery } from "@/services/graphql/composable";
import { stageGraph } from "@/services/graphql";
import DataTable from "@/components/DataTable";
import Modal from "../Modal";
import ActionButtons from "./ActionButtons";
import Detail from "./Detail";
import { displayName } from "@/utils/auth";

const headers = [
  {
    title: "Stage name",
    description: "Name (url)",
    slot: "name",
  },
  {
    title: "Owner",
    description: "Creator of the stage",
    render: (item) => displayName(item.owner),
  },
  {
    title: "Detail",
    description: "Duplicate/Manage stage",
    slot: "detail",
    align: "center",
  },
  {
    title: "Edit Stage",
    slot: "edit",
    align: "center",
  },
];
</script>

<style scoped>
i.fas {
  cursor: pointer;
}
</style>