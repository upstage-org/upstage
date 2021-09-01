<template>
  <div v-if="reactionVisibility" @click="showReactions(false)">
    <div class="icon is-large">
      <Icon src="clear.svg" size="36" />
    </div>
    <span class="tag is-light is-block">Hide reactions</span>
  </div>
  <div v-else @click="showReactions(true)">
    <div class="icon is-large">
      <Icon src="change-nickname.svg" size="36" />
    </div>
    <span class="tag is-light is-block">Show reactions</span>
  </div>
  <div v-if="chatVisibility" @click="showChat(false)">
    <div class="icon is-large">
      <Icon src="clear.svg" size="36" />
    </div>
    <span class="tag is-light is-block">Hide chat</span>
  </div>
  <div v-else @click="showChat(true)">
    <div class="icon is-large">
      <Icon src="change-nickname.svg" size="36" />
    </div>
    <span class="tag is-light is-block">Show chat</span>
  </div>
  <div @click="clearChat">
    <div class="icon is-large">
      <Icon src="erase.svg" size="36" />
    </div>
    <span class="tag is-light is-block">Clear chat</span>
  </div>
  <div @click="toggleChatPosition">
    <div class="icon is-large">
      <Icon v-if="chatPosition === 'right'" src="right-chat.png" size="36" />
      <Icon v-else src="left-chat.png" size="36" />
    </div>
    <span class="tag is-light is-block">Chat Position</span>
  </div>
  <div>
    <div class="icon is-large">
      <ColorPicker v-model="backdropColor" @update:modelValue="sendBackdropColor" />
    </div>
    <span class="tag is-light is-block p-0">Backdrop Color</span>
  </div>
</template>

<script>
import Icon from "@/components/Icon";
import ColorPicker from "@/components/form/ColorPicker";
import { useStore } from "vuex";
import { computed } from "@vue/runtime-core";
import { notification } from "@/utils/notification";
export default {
  components: { Icon, ColorPicker },
  setup: () => {
    const store = useStore();
    const chatVisibility = computed(
      () => store.state.stage.settings.chatVisibility
    );
    const reactionVisibility = computed(
      () => store.state.stage.settings.reactionVisibility
    );

    const showChat = (value) => {
      store.dispatch("stage/showChatBox", value);
    };

    const showReactions = (value) => {
      store.dispatch("stage/showReactionsBar", value);
    };

    const clearChat = () => {
      store.dispatch("stage/clearChat").then(() => {
        notification.success("Chat cleared successfully!");
      });
    };

    const backdropColor = computed(() => store.state.stage.backdropColor);
    const sendBackdropColor = (color) => {
      store.dispatch("stage/setBackdropColor", color);
    };

    const chatPosition = computed(() => store.state.stage.chatPosition);
    const toggleChatPosition = () => {
      store.dispatch(
        "stage/setChatPosition",
        chatPosition.value === "left" ? "right" : "left"
      );
    };

    return {
      showChat,
      chatVisibility,
      showReactions,
      reactionVisibility,
      clearChat,
      sendBackdropColor,
      backdropColor,
      chatPosition,
      toggleChatPosition,
    };
  },
};
</script>

<style>
</style>