<template>
  <transition name="fade">
    <img v-if="fallback && !noFallback" src="assets/notfound.svg" />
    <img
      v-else
      v-bind="$props"
      :key="src"
      :style="{
        'object-fit': fit,
        opacity,
        transform: `rotate(${rotate}deg)`,
      }"
      @error="fallback = true"
    />
  </transition>
</template>

<script>
import { computed, ref } from "vue";
import { watch } from "vue";
export default {
  props: {
    src: {
      type: String,
      required: true,
    },
    fit: {
      type: String,
      default: "contain",
    },
    transition: {
      type: Number,
      default: 1000,
    },
    noFallback: {
      type: Boolean,
      default: false,
    },
    rotate: {
      type: Number,
      default: 0,
    },
    opacity: {
      type: Number,
      default: 1,
    },
  },
  setup: (props) => {
    const fallback = ref(false);
    watch(
      () => props.src,
      () => (fallback.value = false),
    );
    const transitionDuration = computed(() => `${props.transition / 1000}s`);
    return { fallback, transitionDuration };
  },
};
</script>

<style scoped>
img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: center;
  will-change: opacity;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity v-bind(transitionDuration);
  position: absolute;
}
.fade-enter,
.fade-leave-to {
  opacity: 0 !important;
}
.fade-enter-active {
  z-index: -1;
}
</style>
