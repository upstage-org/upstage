<template>
  <button
    v-if="clearChatVisibility"
    class="chat-setting button is-rounded is-outlined"
    @click="clearChat"
    :class="{ 'is-loading': clearing }"
  >
    <span class="icon">
      <Icon src="clear.svg" size="20" />
    </span>
  </button>
</template>

<script>
import { ref } from "vue";
import { message } from "ant-design-vue";
import Icon from "components/Icon.vue";
import buildClient from "services/mqtt";
import { TOPICS } from "utils/constants";
import { namespaceTopic } from "store/modules/stage/reusable";
import { useRoute } from "vue-router";
import { useStore } from "vuex";
import { computed } from "vue";
const mqttClient = buildClient();

export default {
  components: { Icon },
  props: { option: String },
  setup: (props) => {
    const clearing = ref(false);
    const route = useRoute();
    const store = useStore();
    console.log(props.option);
    const clearChat = async () => {
      clearing.value = true;
      await new Promise((resolve) => {
        mqttClient.connect().on("connect", () => {
          const topicChat = namespaceTopic(TOPICS.CHAT, route.params.url);
          if (props.option == "public-chat") {
            mqttClient
              .sendMessage(topicChat, { clear: true }, true)
              .then(resolve);
          } else {
            mqttClient
              .sendMessage(topicChat, { clearPlayerChat: true }, true)
              .then(resolve);
          }
        });
      });
      clearing.value = false;
      if (props.option == "public-chat") {
        message.success(`Chat cleared successfully!`);
      } else {
        message.success(`Player chat cleared successfully!`);
      }
    };

    const clearChatVisibility = computed(
      () => store.state.stage.showClearChatSetting,
    );

    return { clearChat, clearing, clearChatVisibility };
  },
};
</script>

<style></style>
