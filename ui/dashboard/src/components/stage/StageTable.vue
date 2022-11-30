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
      <router-link :to="`/${item.fileLocation}`" class="button is-small is-primary" @click="updateLastAccess(item.dbId)" >
        <span>{{ $t("enter") }}</span>
        <span class="icon">
          <i class="fas fa-chevron-right"></i>
        </span>
      </router-link>
    </template>
    <template #status="{ item }">
      <div class="field is-narrow" v-if="item.permission === 'editor' || item.permission === 'owner' || isAdmin">  
        <Switch
          :data-tooltip="item.status === 'live' ? 'Live' : 'Rehearsal'"
          :model-value="item.status === 'live'"
          @update:model-value="
            (item.status = $event ? 'live' : 'rehearsal'),
            updateStageStatus(item.id)
          "
        />
      </div>
      <span v-else data-tooltip="You don't have edit permission on this stage">🙅‍♀️🙅‍♂️</span>
    </template>
    <template #visibility="{ item }">
      <div class="field is-narrow" v-if="item.permission === 'editor' || item.permission === 'owner' || isAdmin">
        <Switch
          :data-tooltip="item.visibility ? 'On' : 'Off'"
          v-model="item.visibility"
          @update:model-value="
            (item.visibility = $event), 
            updateStageVisibility(item.id)
          "
        />
      </div>
      <span v-else data-tooltip="You don't have edit permission on this stage">🙅‍♀️🙅‍♂️</span>
    </template>
  </DataTable>
</template>

<script>
import DataTable from "@/components/DataTable/index";
import PlayerAudienceCounter from "./PlayerAudienceCounter";
import RecordActions from "./RecordActions";
import { displayName } from "@/utils/auth";
import { computed, inject } from "@vue/runtime-core";
import { useStore } from "vuex";
import Switch from "@/components/form/Switch.vue";
import { stageGraph } from "@/services/graphql";
import { notification } from "@/utils/notification";
import { useMutation } from "@/services/graphql/composable";

export default {
  components: {
    DataTable,
    PlayerAudienceCounter,
    RecordActions,
    Switch
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
        title: "Create Date",
        description: "date of creation",
        render: (item) => formatDate(item.createdOn),
      },
      {
        title: "Last Access",
        description: "date last used / accessed",
        render: (item) => formatDate(item.lastAccess),
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
        title: "Manage",
        slot: "manage",
        align: "center",
      },
      {
        title: "Status",
        slot: "status",
        align: "center",
      },
      {
        title: "Visibility",
        slot: "visibility",
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

    const formatDate = (val) => {
      if (val == null) {
        return null;
      }
      let date = new Date(val);
      let year = date.getFullYear();
      let month = (1 + date.getMonth()).toString().padStart(2, '0');
      let day = date.getDate().toString().padStart(2, '0');
    
      return month + '/' + day + '/' + year;
    }
    const store = useStore();
    const isAdmin = computed(() => store.getters["user/isAdmin"]);

    const updateLastAccess = (stageId) => {
      try {
        const { mutation } = useMutation(stageGraph.updateLastAccess, stageId);
        mutation().then((res) => {
          refresh()
          return res.updateLastAccess.result;
        });
      } catch (error) {
        notification.error(error);
      }
    }
    return { headers, isAdmin, updateLastAccess };
  },
  methods: {
    async updateStageStatus(stageId) {
      try {
        const { mutation } = useMutation(stageGraph.updateStatus, stageId);
        await mutation().then((res) => {
          notification.success("Stage Status updated successfully!");
          return res.updateStatus.result;
        });
      } catch (error) {
        notification.error(error);
      }
    },
    async updateStageVisibility(stageId) {
      try {
        const { mutation } = useMutation(stageGraph.updateVisibility, stageId);
        await mutation().then((res) => {
          notification.success("Stage Visibility updated successfully!");
          return res.updateVisibility.result;
        });
      } catch (error) {
        notification.error(error);
      }
    },

  },
};
</script>

<style scoped>
i.fas {
  cursor: pointer;
}
</style>