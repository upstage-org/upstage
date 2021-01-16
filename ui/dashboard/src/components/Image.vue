<template>
  <img
    v-bind="$props"
    :style="{
      'object-fit': fit,
      opacity,
      transform: `rotate(${rotate ?? 0}deg)`,
    }"
  />
</template>

<script>
export default {
  props: ["src", "fit", "opacity", "rotate"],
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