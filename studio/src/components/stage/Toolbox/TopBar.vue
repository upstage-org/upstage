<template>
  <div id="topbar" class="card is-light" v-if="tool">
    <div
      ref="bar"
      class="card-content"
      :class="{ 'is-compact': compact }"
      :id="tool + 'tool'"
      @wheel="horizontalScroll"
    >
      <component :is="tool" />
    </div>
  </div>
</template>

<script>
import { onUnmounted, ref } from "vue";
import Avatars from "./tools/Avatars.vue";
import Backdrops from "./tools/Backdrops.vue";
import Props from "./tools/Props.vue";
import Audio from "./tools/Audio.vue";
import Draw from "./tools/Draw/index.vue";
import Whiteboard from "./tools/Whiteboard.vue";
import Streams from "./tools/Streams/index.vue";
import Meeting from "./tools/Meeting/index.vue";
import Text from "./tools/Text.vue";
import Settings from "./tools/Settings.vue";
import Depth from "./tools/Depth.vue";
import Curtain from "./tools/Curtain.vue";
import Scenes from "./tools/Scenes/index.vue";

export default {
  props: ["tool"],
  components: {
    Avatars,
    Backdrops,
    Props,
    Audio,
    Draw,
    Streams,
    Meeting,
    Text,
    Settings,
    Depth,
    Curtain,
    Scenes,
    Whiteboard,
  },
  setup: () => {
    const bar = ref();
    const horizontalScroll = (e) => {
      bar.value.scrollLeft += e.deltaY * 10;
      bar.value.scrollLeft += e.deltaX;
    };

    const compact = ref(false);

    const toggleCompact = (e) => {
      if (!e) e = window.event;
      if (e.shiftKey) {
        compact.value = true;
      } else {
        compact.value = false;
      }
    };
    window.addEventListener("keydown", toggleCompact);
    window.addEventListener("keyup", toggleCompact);

    onUnmounted(() => {
      window.removeEventListener("keydown", toggleCompact);
      window.removeEventListener("keyup", toggleCompact);
    });

    return { horizontalScroll, bar, compact };
  },
};
</script>

<style lang="scss">

#topbar {
  display: flex;
  flex: 1;
  position: fixed;
  max-width: 80vw;
  height: 100px;
  top: -12px;
  left: 0;
  right: 0;
  margin: auto;
  text-align: center;
  width: fit-content;
  overflow: hidden;
  z-index: 5;

  &:hover {
    overflow-x: auto;
  }

  .card-content {
    display: flex;
    padding: 0;
    padding-top: 12px;
    min-height: min-content;
    white-space: nowrap;

    &.is-compact {
      width: 100%;
    }

    > div {
      position: relative;
      width: 100px;
      height: 88px;
      background: #F5F5F5;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      border-radius: 8px;

      > div {
        padding: 12px;
      }

      &:first-child {
        float: left;
      }

      .tag {
        height: 1.5em;
        padding: 0;
        box-shadow: none;
      }

      &:hover,
      &.active {
        cursor: pointer;
        filter: brightness(1.2);
        background-color: lightgray;
        img {
          -webkit-filter: drop-shadow(5px 5px 5px #F5F5F5);
          filter: drop-shadow(5px 5px 5px #F5F5F5);
        }
        .tag {
          background-color: transparent;
        }
      }
    }
  }
}
</style>
