<template>
  <button class="button ml-2 is-warning" @click="sweep">
    <template v-if="status">
      <button class="button is-warning is-loading"></button>
      <span>{{ status }}</span>
    </template>
    <span v-else
      ><slot>{{ $t("sweep_stage") }}</slot></span
    >
  </button>
</template>

<script>
import { inject, ref } from "vue";
import { message } from "ant-design-vue";
import { useMutation } from "services/graphql/composable";
import { stageGraph } from "services/graphql";
import { useClearStage } from "components/stage/composable";

export default {
  setup: () => {
    const stage = inject("stage");
    const refresh = inject("refresh");
    const status = ref();
    const { mutation } = useMutation(stageGraph.sweepStage, {
      id: stage.value.id,
    });

    const sweep = async () => {
      try {
        status.value = "Sweeping archived events...";
        await mutation();
        status.value = "Send live stage sweeping signal...";
        const clearStage = useClearStage(stage.value.fileLocation);
        await clearStage();
        message.success(`${stage.value.name} swept successfully!`);
        if (refresh) {
          refresh(stage.value.id);
        }
      } catch (error) {
        message.warning(error);
      } finally {
        status.value = "";
      }
    };

    return { status, sweep };
  },
};
</script>

<style></style>
