<template>
  <div id="topbar" class="card is-light" v-if="tool">
    <div ref="bar" class="card-content" @wheel="horizontalScroll">
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
import Stream from "./tools/Stream";
import Text from "./tools/Text";

export default {
  props: ["tool"],
  components: { Avatars, Backdrop, Props, Audio, Draw, Stream, Text },
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
  position: fixed;
  z-index: 50;
  max-width: 80vw;
  height: 100px;
  top: -12px;
  left: 0;
  right: 0;
  margin: auto;
  text-align: center;
  width: fit-content;
  background-color: rgba($color: white, $alpha: 0.5);
  overflow: visible;
  .card-content {
    padding: 0;
    padding-top: 12px;
    overflow-x: auto;
    white-space: nowrap;

    > div {
      width: 100px;
      height: 88px;
      display: inline-block;
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
        background-color: $primary;
      }
    }
  }
}
</style>