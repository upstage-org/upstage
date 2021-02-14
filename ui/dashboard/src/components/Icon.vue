<template>
  <img :src="path" />
</template>

<script>
import config from "@/../vue.config";
import { computed } from "vue";

export default {
  props: ["src"],
  setup: (props) => {
    const path = computed(() => `${config.publicPath}icons/${props.src}`);
    return { path };
  },
};
</script>

<style lang="scss" scoped>
img {
  width: 100%;
  height: 100%;
}
</style>