<template>
  <audio controls v-if="asset.assetType.name === 'audio'" :src="src"></audio>
  <img v-else :src="src" />
</template>

<script>
import { computed } from "@vue/runtime-core";
import { absolutePath } from "@/utils/common";
export default {
  props: ["asset"],
  setup: (props) => {
    const src = computed(() => absolutePath(props.asset.fileLocation));
    return { src };
  },
};
</script>

<style>
</style>