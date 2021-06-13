<template>
  <div
    data-tooltip="This is a multiframe media"
    class="has-tooltip-bottom"
    v-if="meta.multi"
  >
    <Icon src="multi-frame.svg" />
    <Image
      v-for="frame in meta.frames"
      :key="frame"
      :src="absolutePath(frame)"
      :style="{ width: 'unset', height: '20px' }"
    />
  </div>
</template>

<script>
import { computed } from "@vue/runtime-core";
import Image from "@/components/Image";
import Icon from "@/components/Icon";
import { absolutePath } from "@/utils/common";
export default {
  props: ["asset"],
  components: { Image, Icon },
  setup: (props) => {
    const meta = computed(() => {
      if (props.asset.description) {
        return JSON.parse(props.asset.description);
      }
      return {};
    });

    return { meta, absolutePath };
  },
};
</script>

<style lang="scss" scoped>
</style>