<template>
  <audio controls v-if="asset.mediaType === 'audio'" :src="src"></audio>
  <video controls v-else-if="asset.mediaType === 'stream'" :src="src"></video>
  <img v-else :src="src" style="max-width: 100%; max-height: 100%" />
</template>

<script>
import { computed } from "@vue/runtime-core";
import { absolutePath } from "@/utils/common";
export default {
  props: ["asset"],
  setup: (props) => {
    const src = computed(
      () => props.asset.base64 ?? absolutePath(props.asset.fileLocation)
    );
    return { src };
  },
};
</script>

<style lang="scss" scoped>
audio,
img {
  max-width: 100%;
  max-height: 100%;
}
</style>