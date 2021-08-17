<script setup>
import { getLarixLink } from "@/utils/streaming";
import { computed } from "@vue/reactivity";
import QRCode from "./QRCode.vue";
import { defineProps } from "vue";

const props = defineProps({
  stream: Object,
  size: Number,
});
const code = computed(() =>
  getLarixLink(props.stream.src, props.stream.sign, props.stream.name)
);
</script>

<template>
  <QRCode :value="code" :size="size" />
</template>

<style>
</style>