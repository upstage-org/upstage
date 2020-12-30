<template>
  <img :src="src" :style="'object-fit: ' + fit" />
</template>

<script>
export default {
  props: ["src", "fit"],
};
</script>

<style scoped>
img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}
</style>