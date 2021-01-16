<template>
  <input
    class="opacity-slider slider is-fullwidth"
    :class="{
      'is-primary': sliderMode === 'opacity',
      'is-warning': sliderMode === 'animation',
      'is-danger': sliderMode === 'speed',
    }"
    step="0.01"
    min="0"
    max="1"
    :value="value"
    type="range"
    :style="{
      top: position.y - 26 + 'px',
      left: position.x - 10 + 'px',
      width: position.h + 'px',
    }"
    v-show="active"
    @input="handleInput"
    @change="handleChange"
    @mousedown.stop="keepActive"
    @mouseover.stop="keepActive"
    @mouseup.stop="keepActive"
  />
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
export default {
  props: ["position", "active", "object"],
  emits: ["update:active"],
  setup: (props, { emit }) => {
    const store = useStore();
    const sliderMode = computed(() => store.state.stage.preferences.slider);
    const maxFrameSpeed = 50;
    const value = computed(() => {
      switch (sliderMode.value) {
        case "opacity":
          return props.object.opacity;
        case "animation":
          return props.object.autoplayFrames == 0
            ? 0
            : maxFrameSpeed / props.object.autoplayFrames;
        default:
          break;
      }
    });

    const changeOpacity = (e) => {
      store.commit("stage/UPDATE_OBJECT", {
        ...props.object,
        opacity: e.target.value,
      });
    };
    const sendChangeOpacity = (e) => {
      store.dispatch("stage/shapeObject", {
        ...props.object,
        opacity: e.target.value,
      });
    };

    const calcAutoplayFrames = (e) =>
      e.target.value == 0 ? 0 : maxFrameSpeed / e.target.value;
    const changeFrameAnimationSpeed = (e) => {
      store.commit("stage/UPDATE_OBJECT", {
        ...props.object,
        autoplayFrames: calcAutoplayFrames(e),
      });
    };
    const sendChangeFrameAnimationSpeed = (e) => {
      store.dispatch("stage/shapeObject", {
        ...props.object,
        autoplayFrames: calcAutoplayFrames(e),
      });
    };

    const keepActive = () => {
      emit("update:active", true);
    };
    const handleInput = (e) => {
      keepActive();
      switch (sliderMode.value) {
        case "opacity":
          changeOpacity(e);
          break;
        case "animation":
          changeFrameAnimationSpeed(e);
          break;
        default:
          break;
      }
    };
    const handleChange = (e) => {
      keepActive();
      switch (sliderMode.value) {
        case "opacity":
          sendChangeOpacity(e);
          break;
        case "animation":
          sendChangeFrameAnimationSpeed(e);
          break;
        default:
          break;
      }
    };

    return { keepActive, handleInput, handleChange, value, sliderMode };
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