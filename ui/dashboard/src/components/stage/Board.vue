<template>
  <div
    id="board"
    @dragenter.prevent
    @dragover.prevent
    @drop.prevent="drop"
    :style="{
      width: stageSize.width + 'px',
      height: stageSize.height + 'px',
      transform:
        'translateX(' +
        stageSize.left +
        'px) translateY(' +
        stageSize.top +
        'px)',
      'background-image': 'url(' + background + ')',
    }"
  >
    <transition-group
      name="stage-avatars"
      :css="false"
      @enter="avatarEnter"
      @leave="avatarLeave"
    >
      <Avatar v-for="avatar in avatars" :key="avatar" :avatar="avatar" />
      <Prop v-for="prop in props" :key="prop" :avatar="prop" />
      <Streamer v-for="stream in streams" :key="stream" :stream="stream" />
      <Drawing v-for="drawing in drawings" :key="drawing" :drawing="drawing" />
      <Text v-for="text in texts" :key="text" :text="text" />
    </transition-group>
  </div>
</template>

<script>
import { computed, watch } from "vue";
import { useStore } from "vuex";
import Avatar from "@/components/objects/Avatar/index";
import Streamer from "@/components/objects/Streamer/index";
import Drawing from "@/components/objects/Drawing";
import Text from "@/components/objects/Text";
import anime from "animejs";

export default {
  components: { Avatar, Prop: Avatar, Streamer, Drawing, Text },
  setup: () => {
    const store = useStore();
    const background = computed(() => store.state.stage.background);
    const stageSize = computed(() => store.getters["stage/stageSize"]);
    const config = computed(() => store.getters["stage/config"]);
    const avatars = computed(() => store.getters["stage/avatars"]);
    const props = computed(() => store.getters["stage/props"]);
    const streams = computed(() => store.getters["stage/streams"]);
    const drawings = computed(() => store.getters["stage/drawings"]);
    const texts = computed(() => store.getters["stage/texts"]);

    const drop = (e) => {
      const avatar = JSON.parse(e.dataTransfer.getData("object"));
      if (e.clientX > 0 && e.clientY > 0) {
        store.dispatch("stage/placeObjectOnStage", {
          ...avatar,
          x: e.clientX - 50 - stageSize.value.left,
          y: e.clientY - 50 - stageSize.value.top,
        });
      }
    };

    const avatarEnter = (el, complete) => {
      anime({
        targets: el.querySelector(".object"),
        scale: [0, 1],
        translateY: [-200, 0],
        duration: config.value.animateDuration,
        easing: "easeInOutQuad",
        complete,
      });
    };
    const avatarLeave = (el, complete) => {
      anime({
        targets: el.querySelector(".object"),
        scale: 0,
        rotate: 180,
        duration: config.value.animateDuration,
        easing: "easeInOutQuad",
        complete,
      });
    };

    watch(background, () => {
      anime({
        targets: "#board",
        opacity: [0, 1],
        duration: 5000,
      });
    });

    return {
      avatars,
      drop,
      avatarEnter,
      avatarLeave,
      props,
      streams,
      drawings,
      texts,
      stageSize,
      background,
    };
  },
};
</script>

<style scoped>
#board {
  position: fixed;
  background-size: cover;
}
</style>