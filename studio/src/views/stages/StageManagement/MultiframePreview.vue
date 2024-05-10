<template>
  <a-tooltip title="This is a multiframe media">
    <div v-if="meta.multi" class="has-tooltip-bottom">
      <Icon src="multi-frame.svg" />
      <Image v-for="frame in meta.frames" :key="frame" :src="absolutePath(frame)"
        :style="{ width: 'unset', height: '20px' }" />
    </div>
  </a-tooltip>
</template>

<script>
import { computed } from "vue";
import Image from "components/Image.vue";
import Icon from "components/Icon.vue";
import { absolutePath } from "utils/common";
export default {
  props: {
    asset: Object,
  },
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

<style lang="scss" scoped></style>
