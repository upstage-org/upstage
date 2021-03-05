<template>
  <div class="skeleton" :style="{ width, height }"></div>
</template>

<script>
export default {
  props: {
    width: {
      type: String,
      default: "100%",
    },
    height: {
      type: String,
      default: "150px",
    },
  },
};
</script>

<style lang="scss" scoped>
.skeleton {
  margin: auto;

  background-image: linear-gradient(
      100deg,
      rgba(255, 255, 255, 0),
      rgba(255, 255, 255, 0.5) 50%,
      rgba(255, 255, 255, 0) 80%
    ),
    linear-gradient(lightgray 20px, transparent 0),
    linear-gradient(lightgray 20px, transparent 0),
    linear-gradient(lightgray 20px, transparent 0),
    linear-gradient(lightgray 20px, transparent 0);

  background-repeat: repeat-y;

  background-size: 25% 200px, /* highlight */ 50% 200px, 100% 200px, 75% 200px,
    70% 200px;

  background-position: 0 0, /* highlight */ 0 0, 0 40px, 0 80px, 0 120px;

  animation: shine 1s infinite;
}

@keyframes shine {
  to {
    background-position: 100% 0, /* move highlight to right */ 0 0, 0 40px,
      0 80px, 0 120px;
  }
}
</style>