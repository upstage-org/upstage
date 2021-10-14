<template>
  <DataTable :data="data" :headers="headers">
    <template #name="{ item }">
      <span class="has-text-weight-bold">{{ item.name }}</span>
    </template>
    <template #manage="{ item }">
      <template
        v-if="
          item.permission === 'editor' || item.permission === 'owner' || isAdmin
        "
      >
        <router-link
          :to="`/backstage/stage-management/${item.id}/`"
          class="button is-light is-small"
          data-tooltip="Go to stage management"
        >
          <i class="fa fa-lg fa-cog has-text-primary"></i>
        </router-link>
        <DuplicateStage :stage="item" />
        <DeleteStage v-if="item.permission === 'owner' || isAdmin" :stage="item" :refresh="refresh">
          <a class="button is-light is-small is-danger" data-tooltip="Delete stage">
            <Icon src="delete.svg" />
          </a>
        </DeleteStage>
      </template>
      <span v-else data-tooltip="You don't have edit permission on this stage">🙅‍♀️🙅‍♂️</span>
    </template>
    <template #statistics="{ item }">
      <PlayerAudienceCounter :stage-url="item.fileLocation" />
    </template>
    <template #recording="{ item }">
      <RecordActions :stage="item" />
    </template>
    <template #enter="{ item }">
      <router-link :to="`/live/${item.fileLocation}`" class="button is-small is-primary">
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
import PlayerAudienceCounter from "./PlayerAudienceCounter";
import RecordActions from "./RecordActions";
import DuplicateStage from "./DuplicateStage.vue";
import DeleteStage from "./DeleteStage.vue";
import Icon from "@/components/Icon";
import { displayName } from "@/utils/auth";
import { computed, inject } from "@vue/runtime-core";
import { useStore } from "vuex";

export default {
  components: {
    DataTable,
    PlayerAudienceCounter,
    RecordActions,
    DuplicateStage,
    DeleteStage,
    Icon
  },
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
        title: "Statistics",
        description: "Players and audiences counter",
        slot: "statistics",
        align: "center",
      },
      {
        title: "Recording",
        description: "Start of stop recording",
        slot: "recording",
        align: "center",
      },
      {
        title: "Manage Stage",
        slot: "manage",
        align: "center",
      },
      {
        title: "Access",
        description: "Your permited access to this stage",
        render: (item) =>
          item.permission[0].toUpperCase() + item.permission.substr(1),
      },
      {
        title: "",
        slot: "enter",
        align: "center",
      },
    ];

    const refresh = inject("refresh");

    const store = useStore();
    const isAdmin = computed(() => store.getters["user/isAdmin"]);

    return { headers, isAdmin, refresh };
  },
};
</script>

<style scoped>
i.fas {
  cursor: pointer;
}
</style>