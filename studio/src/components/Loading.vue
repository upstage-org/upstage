<template>
  <img src="assets/loading.svg" :style="{ width, height }" />
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
