<template>
  <div id="topbar" class="card is-light" v-if="tool">
    <div
      ref="bar"
      class="card-content"
      :id="tool + 'tool'"
      @wheel="horizontalScroll"
    >
      <component :is="tool" />
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import Avatars from "./tools/Avatars";
import Backdrop from "./tools/Backdrop";
import Props from "./tools/Props";
import Audio from "./tools/Audio";
import Draw from "./tools/Draw/index";
import Stream from "./tools/Stream/index";
import Text from "./tools/Text";
import Setting from "./tools/Setting";
import Depth from "./tools/Depth";
import Curtain from "./tools/Curtain";
import Scene from "./tools/Scene";

export default {
  props: ["tool"],
  components: {
    Avatars,
    Backdrop,
    Props,
    Audio,
    Draw,
    Stream,
    Text,
    Setting,
    Depth,
    Curtain,
    Scene,
  },
  setup: () => {
    const bar = ref();
    const horizontalScroll = (e) => {
      bar.value.scrollLeft += e.deltaY * 10;
      bar.value.scrollLeft += e.deltaX;
    };
    return { horizontalScroll, bar };
  },
};
</script>

<style lang="scss">
@import "@/styles/bulma";
@import "@/styles/mixins";

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
  overflow-x: auto;
  z-index: 2;

  .card-content {
    display: flex;
    padding: 0;
    padding-top: 12px;
    min-height: min-content;
    white-space: nowrap;

    > div {
      position: relative;
      width: 100px;
      height: 88px;
      padding: 12px;
      background: $light;

      &:first-child {
        float: left;
      }

      .tag {
        height: 1.5em;
        box-shadow: none;
      }

      &:hover,
      &.active {
        cursor: pointer;
        background-color: lightgray;
        img {
          -webkit-filter: drop-shadow(5px 5px 5px $dark);
          filter: drop-shadow(5px 5px 5px $dark);
        }
        .tag {
          background-color: transparent;
        }
      }
    }
  }
}
</style>