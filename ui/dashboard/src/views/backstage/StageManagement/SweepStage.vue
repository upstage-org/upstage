<template>
  <button
    class="button ml-2 is-warning"
    @click="clearChat"
    :class="{ 'is-loading': clearing }"
  >
    Clear Chat
  </button>
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
import { TOPICS } from "@/utils/constants";
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
        status.value = "Sweeping...";
        await mutation();
        status.value = "Clearing broker retained messages...";
        await new Promise((resolve) => {
          mqttClient.connect().on("connect", () => {
            const promisese = Object.keys(TOPICS)
              .map((key) =>
                namespaceTopic(TOPICS[key], stage.value.fileLocation)
              )
              .map((topic) => mqttClient.sendMessage(topic, undefined, true));
            Promise.all(promisese).then(resolve);
          });
        });
        notification.success(`${stage.value.name} swept successfully!`);
      } catch (error) {
        notification.warning(error);
      } finally {
        status.value = "";
      }
    };

    const clearing = ref(false);
    const clearChat = async () => {
      clearing.value = true;
      await new Promise((resolve) => {
        mqttClient.connect().on("connect", () => {
          const topicChat = namespaceTopic(
            TOPICS.CHAT,
            stage.value.fileLocation
          );
          mqttClient
            .sendMessage(topicChat, { clear: true }, true)
            .then(resolve);
        });
      });
      clearing.value = false;
      notification.success(`Chat cleared successfully!`);
    };

    return { status, sweep, clearChat, clearing };
  },
};
</script>

<style>
</style>