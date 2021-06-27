<template>
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
  <div>
    <div class="icon is-large">
      <ColorPicker
        v-model="backdropColor"
        @update:modelValue="sendBackdropColor"
      />
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

    const showChat = (value) => {
      store.dispatch("stage/showChatBox", value);
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

    return {
      showChat,
      chatVisibility,
      clearChat,
      sendBackdropColor,
      backdropColor,
    };
  },
};
</script>

<style>
</style>