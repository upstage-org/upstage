<template>
  <a
    @click="togglePlayerChat"
    :class="{ 'is-active': showPlayerChat }"
    class="panel-block button has-tooltip-right"
    data-tooltip="Player Chat"
  >
    <span class="panel-icon">
      <Icon src="chat.svg" />
    </span>
  </a>
</template>

<script>
import Icon from "@/components/Icon";
import { useStore } from "vuex";
import { computed } from "@vue/runtime-core";
export default {
  components: { Icon },
  setup: () => {
    const store = useStore();
    const showPlayerChat = computed(() => store.state.stage.showPlayerChat);
    const togglePlayerChat = () => {
      store.commit("stage/SET_SHOW_PLAYER_CHAT", !showPlayerChat.value);
    };

    return { showPlayerChat, togglePlayerChat };
  },
};
</script>

<style>
</style>