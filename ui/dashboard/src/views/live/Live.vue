<template>
  <section
    id="live-stage"
    class="hero bg-cover has-background-primary-light is-fullheight"
    :style="'background-image: url(' + background + ')'"
  >
    <ConnectionStatus />
    <Toolbox />
    <Chat />
  </section>
</template>

<script>
import ConnectionStatus from "@/components/stage/ConnectionStatus.vue";
import Chat from "@/components/stage/Chat";
import Toolbox from "@/components/tools/Toolbox";
import { useStore } from "vuex";
import { computed, onMounted, onUnmounted } from "vue";

export default {
  components: { Chat, Toolbox, ConnectionStatus },
  setup: () => {
    const store = useStore();
    onMounted(() => {
      store.dispatch("stage/connect");
    });

    onUnmounted(() => {
      store.dispatch("stage/disconnect");
    });

    return {
      background: computed(() => store.state.stage.background),
    };
  },
};
</script>

<style scoped>
#live-stage {
  background-size: contain;
  background-position: center;
}
</style>