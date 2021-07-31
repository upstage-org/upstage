<template>
  <DataTable :data="scenes" :headers="headers">
    <template #preview="{ item }">
      <img :src="item.scenePreview" />
    </template>
    <template #actions="{ item }">
      <Confirm
        @confirm="(complete) => deleteScene(item, complete)"
        :loading="loading"
      >
        Are you sure you want to delete scene <b> {{ item.name }}</b
        >?
        <template #trigger>
          <a class="button is-danger is-light">
            <Icon src="delete.svg" />
          </a>
        </template>
      </Confirm>
    </template>
  </DataTable>
</template>

<script>
import DataTable from "@/components/DataTable";
import Confirm from "@/components/Confirm";
import Icon from "@/components/Icon";
import { inject, ref } from "@vue/runtime-core";
import { displayName } from "@/utils/auth";
import { useMutation } from "@/services/graphql/composable";
import { stageGraph } from "@/services/graphql";
import { notification } from "@/utils/notification";
export default {
  components: { DataTable, Confirm, Icon },
  setup() {
    const stage = inject("stage");
    const scenes = ref(stage.value.scenes);
    const headers = [
      {
        title: "Preview",
        slot: "preview",
        align: "center",
      },
      {
        title: "Name",
        key: "name",
      },
      {
        title: "Created On",
        key: "createdOn",
        type: "date",
      },
      {
        title: "Created By",
        key: "createdBy",
        render: (item) => displayName(item.owner),
      },
      {
        title: "",
        slot: "actions",
        align: "center",
      },
    ];

    const { mutation, loading } = useMutation(stageGraph.deleteScene);
    const deleteScene = async (scene, complete) => {
      const result = await mutation(scene.id);
      if (result.deleteScene) {
        const { message, success } = result.deleteScene;
        if (success) {
          notification.success(message);
          scenes.value = scenes.value.filter((s) => s.id !== scene.id);
          stage.value.scenes = scenes.value;
        } else {
          notification.error(message);
        }
      }
      complete();
    };

    return { scenes, headers, stage, deleteScene, loading };
  },
};
</script>

<style>
</style>