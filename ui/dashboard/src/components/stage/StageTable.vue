<template>
  <DataTable :data="data" :headers="headers">
    <template #name="{ item }">
      <span class="has-text-weight-bold">{{ item.name }}</span>
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
      <template
        v-if="item.permission === 'editor' || item.permission === 'owner'"
      >
        <router-link
          :to="`/backstage/stage-management/${item.id}/`"
          class="button is-light is-small"
          data-tooltip="Go to stage management"
        >
          <i class="fa fa-lg fa-cog has-text-primary"></i>
        </router-link>
        <router-link
          :to="`/backstage/stage-management/${item.id}/`"
          class="button is-light is-small"
          data-tooltip="Duplicate stage"
        >
          <i class="fa fa-lg fa-clone has-text-warning"></i>
        </router-link>
        <Confirm
          v-if="item.permission === 'owner'"
          @confirm="(complete) => deleteStage(item, complete)"
          :loading="loading"
        >
          Deleting <b>{{ item.name }}</b> will also remove all records and chat
          that ever happened on this stage, there is no undo!
          <span class="has-text-danger">
            Are you sure you want to delete this stage?
          </span>
          <template #trigger>
            <a
              class="button is-light is-small is-danger"
              data-tooltip="Delete stage"
            >
              <Icon src="delete.svg" />
            </a>
          </template>
        </Confirm>
      </template>
      <span v-else data-tooltip="You don't have edit permission on this stage">
        🙅‍♀️🙅‍♂️
      </span>
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
import Modal from "@/components/Modal";
import Confirm from "@/components/Confirm";
import Icon from "@/components/Icon";
import ActionButtons from "./ActionButtons";
import Detail from "./Detail";
import { displayName } from "@/utils/auth";
import { stageGraph } from "@/services/graphql";
import { useMutation } from "@/services/graphql/composable";
import { inject } from "@vue/runtime-core";

export default {
  components: { DataTable, Modal, ActionButtons, Detail, Confirm, Icon },
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
        title: "Access",
        description: "Your permited access to this stage",
        render: (item) =>
          item.permission[0].toUpperCase() + item.permission.substr(1),
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

    const { save, loading } = useMutation(stageGraph.deleteStage);
    const refresh = inject("refresh");
    const deleteStage = async (item, complete) => {
      await save("Stage deleted successfully!", item.id);
      complete();
      if (refresh) {
        refresh();
      }
    };

    return { headers, deleteStage, loading };
  },
};
</script>

<style scoped>
i.fas {
  cursor: pointer;
}
</style>