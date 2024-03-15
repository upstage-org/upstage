<script setup>
import { defineProps } from "vue";
import Confirm from "components/CustomConfirm.vue";
import { stageGraph } from "services/graphql";
import { useMutation } from "services/graphql/composable";

const props = defineProps({
  stage: Object,
  refresh: Function,
});

const { save, loading } = useMutation(stageGraph.deleteStage);
const deleteStage = async (complete) => {
  await save("Stage deleted successfully!", props.stage.id);
  complete();
  if (props.refresh) {
    props.refresh();
  }
};
</script>

<template>
  <Confirm @confirm="(complete) => deleteStage(complete)" :loading="loading">
    <p>
      Deleting
      <b>{{ stage.name }}</b> will also remove all records and chat that ever
      happened on this stage, there is no undo!
      <span class="has-text-danger"
        >Are you sure you want to delete this stage?</span
      >
    </p>
    <br />
    <p>
      If you would like to download the stage's archives before deleting it,
      please click
      <router-link
        :to="`/stages/stage-management/${stage.id}/archive`"
        :data-tooltip="`Archives of ${stage.name}`"
      >
        <b>{{ $t("here") }}</b> </router-link
      >.
    </p>
    <template #trigger>
      <slot></slot>
    </template>
  </Confirm>
</template>
