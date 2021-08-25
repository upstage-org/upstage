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
        <Confirm
          v-if="item.permission === 'owner' || isAdmin"
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
    <template #statistics="{ item }">
      <PlayerAudienceCounter :stage-url="item.fileLocation" />
    </template>
    <template #recording="{ item }">
      <RecordActions :stage="item" />
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
import Confirm from "@/components/Confirm";
import Icon from "@/components/Icon";
import PlayerAudienceCounter from "./PlayerAudienceCounter";
import RecordActions from "./RecordActions";
import DuplicateStage from "./DuplicateStage.vue";
import { displayName } from "@/utils/auth";
import { stageGraph } from "@/services/graphql";
import { useMutation } from "@/services/graphql/composable";
import { computed, inject } from "@vue/runtime-core";
import { useStore } from "vuex";

export default {
  components: {
    DataTable,
    Confirm,
    Icon,
    PlayerAudienceCounter,
    RecordActions,
    DuplicateStage,
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

    const { save, loading } = useMutation(stageGraph.deleteStage);
    const refresh = inject("refresh");
    const deleteStage = async (item, complete) => {
      await save("Stage deleted successfully!", item.id);
      complete();
      if (refresh) {
        refresh();
      }
    };
    const store = useStore();
    const isAdmin = computed(() => store.getters["user/isAdmin"]);

    return { headers, deleteStage, loading, isAdmin };
  },
};
</script>

<style scoped>
i.fas {
  cursor: pointer;
}
</style>