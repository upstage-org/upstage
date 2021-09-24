<template>
  <transition name="fade">
    <img v-if="fallback" src="@/assets/notfound.svg" />
    <img
      v-else
      v-bind="$props"
      :key="src"
      :style="{
        'object-fit': fit,
        opacity,
        transform: `rotate(${rotate ?? 0}deg)`,
      }"
      @error="fallback = true"
    />
  </transition>
</template>

<script>
import { computed, ref } from "@vue/reactivity";
import { watch } from "@vue/runtime-core";
export default {
  props: ["src", "fit", "opacity", "rotate", "transition"],
  setup: (props) => {
    const fallback = ref(false);
    watch(
      () => props.src,
      () => (fallback.value = false)
    );
    const transitionDuration = computed(() => `${props.transition / 1000}s`)
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
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity v-bind(transitionDuration);
  position: absolute;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>