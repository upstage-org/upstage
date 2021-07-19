<template>
  <button class="button ml-2 is-warning" @click="sweep">
    <template v-if="status">
      <button class="button is-warning is-loading"></button>
      <span>{{ status }}</span>
    </template>
    <span v-else>Sweep Stage</span>
  </button>
</template>

<script>
import { inject, ref } from "@vue/runtime-core";
import { useMutation } from "@/services/graphql/composable";
import { stageGraph } from "@/services/graphql";
import { notification } from "@/utils/notification";
import buildClient from "@/services/mqtt";
import { BACKGROUND_ACTIONS, TOPICS } from "@/utils/constants";
import { namespaceTopic } from "@/store/modules/stage/reusable";

const mqttClient = buildClient();

export default {
  setup: () => {
    const stage = inject("stage");
    const status = ref();
    const { mutation } = useMutation(stageGraph.sweepStage, {
      id: stage.value.id,
    });
    const sweep = async () => {
      try {
        status.value = "Sweeping archived events...";
        await mutation();
        status.value = "Send live stage sweeping signal...";
        await new Promise((resolve) => {
          mqttClient.connect().on("connect", () => {
            mqttClient
              .sendMessage(
                namespaceTopic(TOPICS.BACKGROUND, stage.value.fileLocation),
                { type: BACKGROUND_ACTIONS.BLANK_SCENE },
                true
              )
              .then(resolve);
          });
        });
        notification.success(`${stage.value.name} swept successfully!`);
      } catch (error) {
        notification.warning(error);
      } finally {
        status.value = "";
      }
    };

    return { status, sweep };
  },
};
</script>

<style>
</style>