<template>
  <img :src="path" :style="{ width: size + 'px', height: size + 'px' }" />
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
  },
  setup: (props) => {
    const path = computed(() => `${config.publicPath}icons/${props.src}`);
    return { path };
  },
};
</script>

<style lang="scss" scoped>
</style>