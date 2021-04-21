<template>
  <button
    class="button mr-2 mt-2 is-warning"
    :class="{ 'is-loading': status }"
    @click="sweep"
  >
    <span v-if="status">{{ status }}</span>
    <span v-else> Clear Chat & Sweep Stage</span>
  </button>
</template>

<script>
import { inject, ref } from "@vue/runtime-core";
import { useMutation } from "@/services/graphql/composable";
import { stageGraph } from "@/services/graphql";
import { notification } from "@/utils/notification";
import mqttService from "@/services/mqtt";
import { TOPICS } from "@/utils/constants";
export default {
  setup: () => {
    const stage = inject("stage");
    const status = ref();
    const { mutation } = useMutation(stageGraph.sweepStage, {
      id: stage.value.id,
    });
    const sweep = async () => {
      try {
        status.value = "Save performance as record";
        await mutation();
        status.value = "Clear the stage";
        await new Promise((resolve) => {
          mqttService.connect().on("connect", () => {
            const promisese = Object.keys(TOPICS)
              .map((key) => `${stage.value.fileLocation}/${TOPICS[key]}`)
              .map((topic) => mqttService.sendMessage(topic, undefined, true));
            console.log(promisese);
            Promise.all(promisese).then(resolve);
          });
        });
      } catch (error) {
        notification.error(error);
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