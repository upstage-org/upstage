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
      <Backdrop />
      <transition-group
        name="stage-avatars"
        :css="false"
        @enter="avatarEnter"
        @leave="avatarLeave"
      >
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
  <Whiteboard />
  <Curtain />
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import Avatar from "@/components/objects/Avatar/index";
import Drawing from "@/components/objects/Drawing";
import Stream from "@/components/objects/Streamer/index";
import Meeting from "@/components/objects/Meeting/index";
import Jitsi from "@/components/objects/Meeting/Jitsi";
import Text from "@/components/objects/Text";
import Curtain from "@/components/stage/Curtain";
import Whiteboard from "@/components/stage/Whiteboard";
import Image from "../Image";
import anime from "animejs";
import Backdrop from "./Backdrop.vue";

export default {
  components: {
    Avatar,
    Prop: Avatar,
    Stream,
    Drawing,
    Text,
    Curtain,
    Whiteboard,
    Image,
    Backdrop,
    Meeting,
    Jitsi,
  },
  setup: () => {
    const store = useStore();
    const canPlay = computed(() => store.getters["stage/canPlay"]);

    const stageSize = computed(() => store.getters["stage/stageSize"]);
    const config = computed(() => store.getters["stage/config"]);
    const objects = computed(() => store.getters["stage/objects"]);

    const drop = (e) => {
      const { object, isReal, nodrop } = JSON.parse(
        e.dataTransfer.getData("text"),
      );
      if (isReal) {
        if (
          confirm("Are you sure you want to take this object out of the stage?")
        ) {
          store.dispatch("stage/deleteObject", object);
        }
      } else {
        if (e.clientX > 0 && e.clientY > 0 && !nodrop) {
          store
            .dispatch("stage/placeObjectOnStage", {
              ...object,
              x: e.clientX - 50 - stageSize.value.left,
              y: e.clientY - 50 - stageSize.value.top,
            })
            .then(({ id }) => {
              store.dispatch("stage/autoFocusMoveable", id);
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

    const backdropColor = computed(() => store.state.stage.backdropColor);

    return {
      objects,
      drop,
      avatarEnter,
      avatarLeave,
      stageSize,
      backdropColor,
      canPlay,
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
</style>
