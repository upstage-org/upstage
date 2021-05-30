<template>
  <img v-if="fallback" src="@/assets/notfound.svg" />
  <img
    v-else
    v-bind="$props"
    :style="{
      'object-fit': fit,
      opacity,
      transform: `rotate(${rotate ?? 0}deg)`,
    }"
    @error="fallback = true"
  />
</template>

<script>
import { ref } from "@vue/reactivity";
import { watch } from "@vue/runtime-core";
export default {
  props: ["src", "fit", "opacity", "rotate"],
  setup: (props) => {
    const fallback = ref(false);
    watch(
      () => props.src,
      () => (fallback.value = false)
    );
    return { fallback };
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
</style>