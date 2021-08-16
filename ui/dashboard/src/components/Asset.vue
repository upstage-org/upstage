<template>
  <audio controls v-if="asset.mediaType === 'audio'" :src="src"></audio>
  <template v-else-if="asset.mediaType === 'stream'">
    <QRCode v-if="meta.isRTMP" :value="getLarixLink(asset.file_location)" />
    <video v-else controls :src="src"></video>
  </template>
  <img
    v-else
    :src="src"
    style="max-width: 100%; max-height: 100%"
    @load="handleLoad"
  />
</template>

<script>
import { computed } from "@vue/runtime-core";
import { absolutePath } from "@/utils/common";
import QRCode from "@/components/QRCode";
import { getLarixLink } from "@/utils/streaming";

export default {
  props: ["asset"],
  emits: ["detectSize"],
  components: { QRCode },
  setup: (props, { emit }) => {
    if (props.asset.assetType) {
      Object.assign(props.asset, { mediaType: props.asset.assetType.name });
    }
    const src = computed(
      () => props.asset.base64 ?? absolutePath(props.asset.src)
    );
    const meta = computed(() => {
      if (props.asset.description) {
        return JSON.parse(props.asset.description);
      }
      return {};
    });
    const handleLoad = (e) => {
      emit("detectSize", {
        width: e.target.width,
        height: e.target.height,
      });
    };

    return { src, meta, handleLoad, getLarixLink };
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