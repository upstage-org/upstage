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
        'background-image': 'url(' + background + ')',
      }"
    >
      <transition-group
        name="stage-avatars"
        :css="false"
        @enter="avatarEnter"
        @leave="avatarLeave"
      >
        <component
          v-for="object in objects"
          :key="object.id"
          :is="object.type ?? 'avatar'"
          :object="object"
        />
      </transition-group>
    </div>
  </section>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import Avatar from "@/components/objects/Avatar/index";
import Drawing from "@/components/objects/Drawing";
import Stream from "@/components/objects/Streamer/index";
import Text from "@/components/objects/Text";
import anime from "animejs";

export default {
  components: { Avatar, Prop: Avatar, Stream, Drawing, Text },
  setup: () => {
    const store = useStore();
    const background = computed(() => {
      const background = store.state.stage.background;
      if (background.multi && background.currentFrame) {
        return background.currentFrame;
      } else {
        return background.src;
      }
    });
    const stageSize = computed(() => store.getters["stage/stageSize"]);
    const config = computed(() => store.getters["stage/config"]);
    const objects = computed(() => store.getters["stage/objects"]);

    const drop = (e) => {
      const { object, isReal } = JSON.parse(e.dataTransfer.getData("text"));
      if (e.clientX > 0 && e.clientY > 0) {
        store.dispatch(
          isReal ? "stage/shapeObject" : "stage/placeObjectOnStage",
          {
            ...object,
            x: e.clientX - 50 - stageSize.value.left,
            y: e.clientY - 50 - stageSize.value.top,
          }
        );
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
      background,
      backdropColor,
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