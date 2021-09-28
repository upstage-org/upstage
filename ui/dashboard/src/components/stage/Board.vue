<template>
  <section
    id="live-stage"
    class="hero bg-cover is-fullheight"
    :style="{ 'background-color': backdropColor }"
  >
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
      }"
    >
      <Image
        class="background-image"
        :src="background"
        :style="{
          opacity: backgroundOpacity,
        }"
        :transition="backgroundSpeed"
      />
      <transition-group name="stage-avatars" :css="false" @enter="avatarEnter" @leave="avatarLeave">
        <component
          v-for="object in objects"
          :id="object.id"
          :key="object.id"
          :is="object.drawingId ? 'drawing' : object.type ?? 'avatar'"
          :object="object"
        />
      </transition-group>
    </div>
  </section>
  <Curtain />
  <Whiteboard />
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import Avatar from "@/components/objects/Avatar/index";
import Drawing from "@/components/objects/Drawing";
import Stream from "@/components/objects/Streamer/index";
import Text from "@/components/objects/Text";
import Curtain from "@/components/stage/Curtain";
import Whiteboard from "@/components/stage/Whiteboard";
import Image from "../Image";
import anime from "animejs";

export default {
  components: {
    Avatar,
    Prop: Avatar,
    Stream,
    Drawing,
    Text,
    Curtain,
    Whiteboard,
    Image
  },
  setup: () => {
    const store = useStore();
    const canPlay = computed(() => store.getters["stage/canPlay"]);
    const background = computed(() => {
      const background = store.state.stage.background ?? {};
      if (background.multi && background.currentFrame) {
        return background.currentFrame;
      } else {
        return background.src;
      }
    });
    const backgroundOpacity = computed(
      () => store.state.stage.background?.opacity ?? 1
    );
    const backgroundSpeed = computed(() => 100 / store.state.stage.background?.speed);
    const stageSize = computed(() => store.getters["stage/stageSize"]);
    const config = computed(() => store.getters["stage/config"]);
    const objects = computed(() => store.getters["stage/objects"]);

    const drop = (e) => {
      const { object, isReal } = JSON.parse(e.dataTransfer.getData("text"));
      if (isReal) {
        if (
          confirm("Are you sure you want to take this object out of the stage?")
        ) {
          store.dispatch("stage/deleteObject", object);
        }
      } else {
        if (e.clientX > 0 && e.clientY > 0) {
          store.dispatch("stage/placeObjectOnStage", {
            ...object,
            x: e.clientX - 50 - stageSize.value.left,
            y: e.clientY - 50 - stageSize.value.top,
          });
        }
      }
    };

    const avatarEnter = (el, complete) => {
      anime({
        targets: el.querySelector(".object"),
        scale: [0, 1],
        translateY: [-200, 0],
        duration: config.value.animateDuration,
        easing: "easeInOutQuad",
        complete: () => {
          store.dispatch("stage/autoFocusMoveable", el.id);
          complete();
        },
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

    const backdropColor = computed(() => store.state.stage.backdropColor);

    return {
      objects,
      drop,
      avatarEnter,
      avatarLeave,
      stageSize,
      background,
      backdropColor,
      canPlay,
      backgroundOpacity,
      backgroundSpeed
    };
  },
};
</script>

<style scoped>
#board {
  position: fixed;
  background-size: cover;
  overflow: hidden;
}
.background-image {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: auto;
}
</style>