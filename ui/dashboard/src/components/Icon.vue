<template>
  <img
    :src="path"
    :style="{ width: (width ?? size) + 'px', height: (height ?? size) + 'px' }"
  />
</template>

<script>
import config from "@/../vue.config";
import { computed } from "vue";

export default {
  props: {
    src: { type: String, required: true },
    size: {
      type: Number,
      default: 16,
    },
    width: Number,
    height: Number,
  },
  setup: (props) => {
    const path = computed(() => `${config.publicPath}icons/${props.src}`);
    return { path };
  },
};
</script>

<style lang="scss" scoped>
</style>