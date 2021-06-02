<template>
  <audio controls v-if="asset.mediaType === 'audio'" :src="src"></audio>
  <template v-else-if="asset.mediaType === 'stream'">
    <RTMPStream v-if="meta.isRTMP" :src="asset.fileLocation"></RTMPStream>
    <video v-else controls :src="src"></video>
  </template>
  <img v-else :src="src" style="max-width: 100%; max-height: 100%" />
</template>

<script>
import { computed } from "@vue/runtime-core";
import { absolutePath } from "@/utils/common";
import RTMPStream from "@/components/RTMPStream";

export default {
  props: ["asset"],
  components: { RTMPStream },
  setup: (props) => {
    if (props.asset.assetType) {
      Object.assign(props.asset, { mediaType: props.asset.assetType.name });
    }
    const src = computed(
      () => props.asset.base64 ?? absolutePath(props.asset.fileLocation)
    );
    const meta = computed(() => {
      if (props.asset.description) {
        return JSON.parse(props.asset.description);
      }
      return {};
    });

    return { src, meta };
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