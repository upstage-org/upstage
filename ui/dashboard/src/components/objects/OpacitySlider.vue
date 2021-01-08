<template>
  <input
    class="opacity-slider slider is-fullwidth is-success"
    step="1"
    min="0"
    max="100"
    value="50"
    type="range"
    :style="{
      top: position.y - 26 + 'px',
      left: position.x - 10 + 'px',
      width: position.h + 'px',
    }"
    v-show="active"
    @input="changeOpacity"
    @change="sendChangeOpacity"
    @mousedown.stop="keepActive"
    @mouseover.stop="keepActive"
    @mouseup.stop="keepActive"
  />
</template>

<script>
import { useStore } from "vuex";
export default {
  props: ["position", "active", "object"],
  emits: ["update:active"],
  setup: (props, { emit }) => {
    const store = useStore();
    const keepActive = () => {
      emit("update:active", true);
    };
    const calcOpacity = (e) => Number(e.target.value) / 100;

    const changeOpacity = (e) => {
      keepActive();
      const opacity = calcOpacity(e);
      store.commit("stage/UPDATE_OBJECT", {
        ...props.object,
        opacity,
      });
    };

    const sendChangeOpacity = (e) => {
      keepActive();
      const opacity = calcOpacity(e);
      store.dispatch("stage/shapeObject", {
        ...props.object,
        opacity,
      });
    };
    return { keepActive, changeOpacity, sendChangeOpacity };
  },
};
</script>

<style>
.opacity-slider {
  position: fixed;
  transform: rotate(270deg) translateX(-100%);
  transform-origin: left;
}
</style>