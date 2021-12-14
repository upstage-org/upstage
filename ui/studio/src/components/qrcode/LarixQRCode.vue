<script setup lang="ts">
import { getLarixLink } from "../../utils/streaming";
import { computed, PropType, watchEffect } from "vue";
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
watchEffect(() => {
  console.log(code.value, props.stream);
});
</script>

<template>
  <a-tooltip :title="props.stream.sign ? null : `You can't broadcast to this stream!`">
    <QRCode
      :value="code"
      :size="size"
      :class="`${props.stream.sign ? '' : 'opacity-50 cursor-not-allowed'}`"
    />
  </a-tooltip>
</template>

<style>
</style>