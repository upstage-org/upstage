<script lang="ts" setup>
import { computed } from "@vue/reactivity";
import { humanFileSize } from "utils/common";

const { value } = defineProps({
  value: {
    type: Number,
    default: 0,
  },
});

const text = computed(() => humanFileSize(value));
</script>

<template>{{ text }}</template>
