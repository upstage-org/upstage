<script setup lang="ts">
import { getLarixLink } from "../../utils/streaming";
import { computed, PropType } from "vue";
import QRCode from "./QRCode.vue";
import { Media } from "../../models/studio";

const props = defineProps({
  stream: { type: Object as PropType<Media>, required: true },
  size: Number,
});
const code = computed(() =>
  getLarixLink(
    props.stream.src,
    props.stream.sign,
    props.stream.name
  )
);
</script>

<template>
  <a-tooltip title="New unique key detected, please save the stream first!">
    <QRCode
      :value="code"
      :size="size"
      :class="`${props.stream.sign ? '' : 'opacity-50 cursor-not-allowed'}`"
    />
  </a-tooltip>
</template>

<style>
</style>