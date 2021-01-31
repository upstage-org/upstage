<template>
  <div id="board" @dragenter.prevent @dragover.prevent @drop.prevent="drop">
    <transition-group
      name="stage-avatars"
      :css="false"
      @enter="avatarEnter"
      @leave="avatarLeave"
    >
      <Avatar v-for="avatar in avatars" :key="avatar" :avatar="avatar" />
      <Prop v-for="prop in props" :key="prop" :avatar="prop" />
      <Streamer v-for="stream in streams" :key="stream" :stream="stream" />
    </transition-group>
  </div>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import Avatar from "@/components/objects/Avatar/index";
import Streamer from "@/components/objects/Streamer/index";
import anime from "animejs";

export default {
  components: { Avatar, Prop: Avatar, Streamer },
  setup: () => {
    const store = useStore();
    const config = store.getters["stage/config"];
    const avatars = computed(() => store.getters["stage/avatars"]);
    const props = computed(() => store.getters["stage/props"]);
    const streams = computed(() => store.getters["stage/streams"]);

    const drop = (e) => {
      const avatar = JSON.parse(e.dataTransfer.getData("object"));
      if (e.clientX > 0 && e.clientY > 0) {
        store.dispatch("stage/placeObjectOnStage", {
          ...avatar,
          x: e.clientX - 50,
          y: e.clientY - 50,
        });
      }
    };

    const avatarEnter = (el, complete) => {
      anime({
        targets: el.getElementsByTagName("img"),
        scale: [0, 1],
        translateY: [-200, 0],
        duration: config.animateDuration,
        easing: "easeInOutQuad",
        complete,
      });
    };
    const avatarLeave = (el, complete) => {
      anime({
        targets: el.getElementsByTagName("img"),
        scale: 0,
        rotate: 180,
        duration: config.animateDuration,
        easing: "easeInOutQuad",
        complete,
      });
    };

    return { avatars, drop, avatarEnter, avatarLeave, props, streams };
  },
};
</script>

<style scoped>
#board {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
}
</style>