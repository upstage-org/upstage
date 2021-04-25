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
</template>

<script>
import Icon from "@/components/Icon";
import { useStore } from "vuex";
import { computed } from "@vue/runtime-core";
export default {
  components: { Icon },
  setup: () => {
    const store = useStore();
    const chatVisibility = computed(
      () => store.state.stage.settings.chatVisibility
    );

    const showChat = (value) => {
      store.dispatch("stage/showChatBox", value);
    };

    return { showChat, chatVisibility };
  },
};
</script>

<style>
</style>