<template>
  <img v-bind="$props" :style="{ 'object-fit': fit, opacity }" />
</template>

<script>
export default {
  props: ["src", "fit", "opacity"],
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