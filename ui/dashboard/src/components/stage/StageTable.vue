<template>
  <DataTable :data="data" :headers="headers">
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
          <button class="button is-light is-small">
            <i class="fas fa-lg fa-eye has-text-primary" />
          </button>
        </template>
        <template #header>Stage Detail</template>
        <template #content><Detail :stage="item" /></template>
        <template #footer><ActionButtons :stage="item" /></template>
      </Modal>
    </template>
    <template #manage="{ item }">
      <router-link
        :to="`/dashboard/stage-management/${item.id}/`"
        class="button is-light is-small"
        data-tooltip="Go to stage management"
      >
        <i class="fa fa-lg fa-cog has-text-primary"></i>
      </router-link>
      <router-link
        :to="`/dashboard/stage-management/${item.id}/`"
        class="button is-light is-small"
        data-tooltip="Duplicate stage"
      >
        <i class="fa fa-lg fa-clone has-text-warning"></i>
      </router-link>
      <router-link
        :to="`/dashboard/stage-management/${item.id}/`"
        class="button is-light is-small"
        data-tooltip="Delete stage"
      >
        <i class="fa fa-lg fa-trash has-text-danger"></i>
      </router-link>
    </template>
    <template #enter="{ item }">
      <router-link
        :to="`/live/${item.fileLocation}`"
        class="button is-small is-primary"
      >
        <span>ENTER</span>
        <span class="icon">
          <i class="fas fa-chevron-right"></i>
        </span>
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

export default {
  components: { DataTable, Modal, ActionButtons, Detail },
  props: { data: Array },
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
        title: "Manage Stage",
        slot: "manage",
        align: "center",
      },
      {
        title: "",
        slot: "enter",
        align: "center",
      },
    ];

    return { headers };
  },
};
</script>

<style scoped>
i.fas {
  cursor: pointer;
}
</style>