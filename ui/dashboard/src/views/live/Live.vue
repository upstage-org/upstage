<template>
  <section
    id="live-stage"
    class="hero bg-cover has-background-primary-light is-fullheight"
    :style="'background-image: url(' + background + ')'"
  >
    <Toolbox />
    <Chat />
  </section>
</template>

<script>
import Chat from "@/components/stage/Chat";
import Toolbox from "@/components/tools/Toolbox";
import { useStore } from "vuex";
import { computed } from "vue";

export default {
  components: { Chat, Toolbox },
  setup: () => {
    const store = useStore();

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