<template>
  <HLSPlayer v-bind="$attrs" :src="fullUrl" />
</template>

<script>
import HLSPlayer from "@/components/HLSPlayer.vue";
import { computed } from "@vue/runtime-core";
import { getSubsribeLink } from "@/utils/rtmp";
export default {
  components: { HLSPlayer },
  props: ["src"],
  setup: (props) => {
    const fullUrl = computed(() => getSubsribeLink(props.src));
    return { fullUrl };
  },
};
</script>

<style>
</style>