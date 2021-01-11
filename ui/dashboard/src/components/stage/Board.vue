<template>
  <div id="board" @dragenter.prevent @dragover.prevent @drop.prevent="drop">
    <transition-group name="stage-avatars" :css="false" @leave="avatarLeave">
      <Avatar v-for="avatar in avatars" :key="avatar" :avatar="avatar" />
    </transition-group>
  </div>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import Avatar from "@/components/objects/Avatar";
import anime from "animejs";

export default {
  components: { Avatar },
  setup: () => {
    const store = useStore();
    const config = store.getters["stage/config"];
    const avatars = computed(() => store.getters["stage/avatars"]);

    const drop = (e) => {
      const avatar = JSON.parse(e.dataTransfer.getData("avatar"));
      if (e.clientX > 0 && e.clientY > 0) {
        store.dispatch("stage/summonAvatar", {
          ...avatar,
          x: e.clientX - 50,
          y: e.clientY - 50,
        });
      }
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

    return { avatars, drop, avatarLeave };
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