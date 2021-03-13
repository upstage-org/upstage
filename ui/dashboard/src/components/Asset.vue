<template>
  <audio controls v-if="asset.assetType?.name === 'audio'" :src="src"></audio>
  <Image v-else :src="src" />
</template>

<script>
import { computed } from "@vue/runtime-core";
import { absolutePath } from "@/utils/common";
import Image from "./Image.vue";
export default {
  components: { Image },
  props: ["asset"],
  setup: (props) => {
    const src = computed(() => absolutePath(props.asset.fileLocation));
    return { src };
  },
};
</script>

<style>
</style>