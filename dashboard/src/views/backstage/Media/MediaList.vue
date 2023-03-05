<template>
  <DataTable :data="mediaList" :headers="headers">
    <template #preview="{ item }">
      <Asset :asset="item" />
      <MultiframePreview :asset="item" />
    </template>
    <template #stage="{ item }">
      <span v-for="(stage, index) in item.stages" :key="stage">
        <router-link :to="`/${stage.url}/`">
          {{ stage.name }}
        </router-link>
        <span v-if="index < item.stages.length - 1">, </span>
      </span>
    </template>
    <template #copyright="{ item }">
      <div :data-tooltip="copyrightLevels[item.copyrightLevel].description">
        {{ copyrightLevels[item.copyrightLevel].name }}
      </div>
    </template>
    <template #manage="{ item }">
      <span v-if="editable(item)" style="float: left">
        <MediaEdit :media="item" />
      </span>
      <a
        v-if="downloadable(item)"
        class="button is-light is-small"
        :href="absolutePath(item.src)"
        :download="item.name"
      >
        <Icon src="download.svg" />
      </a>
      <Confirm
        v-if="deletable(item)"
        @confirm="(complete) => deleteMedia(item, complete)"
        :loading="loading"
      >
        Are you sure you want to delete <b>{{ item.name }}</b
        >? It will be completely emoved from the UpStage server.
        <span class="has-text-danger">There is no undo!</span> If you only
        wanted to remove it from a stage, please go to Stage Management and
        unassign it.
        <template #trigger>
          <a class="button is-light is-small is-danger">
            <Icon src="delete.svg" />
          </a>
        </template>
      </Confirm>
    </template>
  </DataTable>
</template>

<script>
import { computed, inject } from "@vue/runtime-core";
import { absolutePath } from "@/utils/common";
import Asset from "@/components/Asset";
import DataTable from "@/components/DataTable/index";
import Confirm from "@/components/Confirm";
import Icon from "@/components/Icon";
import MediaEdit from "./MediaEdit";
import { displayName } from "@/utils/auth";
import { useMutation } from "@/services/graphql/composable";
import { stageGraph } from "@/services/graphql";
import { notification } from "@/utils/notification";
import MultiframePreview from "./MultiframePreview";
import { MEDIA_COPYRIGHT_LEVELS } from "@/utils/constants";
import { useStore } from "vuex";

export default {
  components: { Asset, MediaEdit, DataTable, Confirm, MultiframePreview, Icon },
  setup: () => {
    const mediaList = inject("mediaList");
    const popNode = inject("popNode");

    const headers = [
      {
        title: "Preview",
        slot: "preview",
        align: "center",
      },
      {
        title: "Name",
        key: "name",
        align: "center",
      },
      {
        title: "Type",
        render: (item) =>
          item.assetType.name === "media" ? "" : item.assetType.name,
      },
      {
        title: "Owner",
        render: (item) => displayName(item.owner),
      },
      {
        title: "Stage",
        slot: "stage",
      },
      {
        title: "Date",
        type: "date",
        key: "createdOn",
      },
      {
        title: "Owner",
        align: "center",
        slot: "copyright",
      },
      {
        title: "Manage Media",
        slot: "manage",
      },
    ];

    const { mutation, loading } = useMutation(stageGraph.deleteMedia);
    const deleteMedia = async (item, complete) => {
      const result = await mutation(item.id);
      if (result.deleteMedia) {
        const { message, success } = result.deleteMedia;
        const notify = success ? notification.success : notification.error;
        notify(message);
        if (popNode) {
          popNode((m) => m.id === item.id);
        }
      }
      complete();
    };

    const store = useStore();
    const isAdmin = computed(() => store.getters["user/isAdmin"]);
    const editable = (item) => ["editor", "owner"].includes(item.permission);
    const downloadable = (item) =>
      ["editor", "owner", "readonly"].includes(item.permission);
    const deletable = (item) =>
      ["owner"].includes(item.permission) || isAdmin.value;

    return {
      mediaList,
      absolutePath,
      headers,
      deleteMedia,
      loading,
      editable,
      downloadable,
      deletable,
      copyrightLevels: MEDIA_COPYRIGHT_LEVELS,
    };
  },
};
</script>

<style>
.media-column {
  position: relative;
}
.type-tag {
  position: absolute;
  z-index: 10;
  top: 20px;
  right: 0;
}
td.preview {
  width: 300px;
}
td.preview img {
  height: 50px;
}
</style>
