<template>
  <section
    id="live-stage"
    class="hero bg-cover has-background-primary-light is-fullheight"
    :style="'background-image: url(' + background + ')'"
  >
    <Board />
    <ConnectionStatus />
    <Toolbox />
    <Chat />
    <AudioPlayer />
  </section>
</template>

<script>
import Chat from "@/components/stage/Chat";
import Toolbox from "@/components/stage/Toolbox";
import ConnectionStatus from "@/components/stage/ConnectionStatus";
import Board from "@/components/stage/Board";
import AudioPlayer from "@/components/stage/AudioPlayer";
import { useStore } from "vuex";
import { computed, onMounted, onUnmounted, watch } from "vue";
import anime from "animejs";

export default {
  components: {
    Chat,
    Toolbox,
    ConnectionStatus,
    Board,
    AudioPlayer,
  },
  setup: () => {
    const store = useStore();
    const background = computed(() => store.state.stage.background);

    onMounted(() => {
      store.dispatch("stage/connect");
    });

    onUnmounted(() => {
      store.dispatch("stage/disconnect");
    });

    watch(background, () => {
      anime({
        targets: "#live-stage",
        opacity: [0, 1],
        duration: 5000,
      });
    });

    const loggedIn = computed(() => store.getters["auth/loggedIn"]);

    return { background, loggedIn };
  },
};
</script>

<style lang="scss">
#live-stage {
  background-size: cover;
  *:not(input) {
    -webkit-touch-callout: none; /* iOS Safari */
    -webkit-user-select: none; /* Safari */
    -khtml-user-select: none; /* Konqueror HTML */
    -moz-user-select: none; /* Old versions of Firefox */
    -ms-user-select: none; /* Internet Explorer/Edge */
    user-select: none; /* Non-prefixed version, currently supported by Chrome, Edge, Opera and Firefox */
  }
}
</style>