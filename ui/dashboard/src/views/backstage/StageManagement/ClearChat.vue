<template>
  <button
    class="button ml-2 is-warning"
    @click="clearChat"
    :class="{ 'is-loading': clearing }"
  >
    Clear Chat
  </button>
</template>

<script>
import { inject, ref } from "@vue/runtime-core";
import { notification } from "@/utils/notification";
import buildClient from "@/services/mqtt";
import { TOPICS } from "@/utils/constants";
import { namespaceTopic } from "@/store/modules/stage/reusable";

const mqttClient = buildClient();

export default {
  setup: () => {
    const stage = inject("stage");
    const refresh = inject("refresh");

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
          mqttClient
            .sendMessage(topicChat, { clearPlayerChat: true }, true)
            .then(resolve);
        });
      });
      clearing.value = false;
      notification.success(`Chat cleared successfully!`);
      refresh(stage.value.id);
    };

    return { clearChat, clearing };
  },
};
</script>

<style>
</style>