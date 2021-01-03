<template>
  <div id="board" @dragenter.prevent @dragover.prevent @drop.prevent="drop">
    <Avatar v-for="avatar in avatars" :key="avatar" :avatar="avatar" />
  </div>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import Avatar from "@/components/objects/Avatar";

export default {
  components: { Avatar },
  setup: () => {
    const store = useStore();
    const avatars = computed(() => store.getters["stage/avatars"]);

    const drop = (e) => {
      const avatar = JSON.parse(e.dataTransfer.getData("avatar"));
      if (e.clientX > 0 && e.clientY > 0) {
        store.dispatch("stage/summonAvatar", {
          ...avatar,
          x: e.clientX - 50,
          y: e.clientY - 50,
          w: 100,
          h: 100,
        });
      }
    };
    return { avatars, drop };
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