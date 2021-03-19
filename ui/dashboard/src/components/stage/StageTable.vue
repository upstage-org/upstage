<template>
  <DataTable :query="stageList" :headers="headers">
    <template #name="{ item }">
      <router-link
        :to="`/live/${item.fileLocation}`"
        class="has-text-primary has-text-weight-bold"
      >
        {{ item.name }}
      </router-link>
    </template>
    <template #detail="{ item }">
      <Modal>
        <template #trigger>
          <i class="fas fa-lg fa-eye" />
        </template>
        <template #header>Stage Detail</template>
        <template #content><Detail :stage="item" /></template>
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

<script>
import DataTable from "@/components/DataTable/index";
import Modal from "../Modal";
import ActionButtons from "./ActionButtons";
import Detail from "./Detail";
import { displayName } from "@/utils/auth";
import { stageGraph } from "@/services/graphql";

export default {
  components: { DataTable, Modal, ActionButtons, Detail },
  setup: () => {
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
    return { headers, stageList: stageGraph.stageList };
  },
};
</script>

<style scoped>
i.fas {
  cursor: pointer;
}
</style>