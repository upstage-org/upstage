<script setup>
import { notification } from "@/utils/notification";
import modernCopy from "modern-copy";
import { defineProps } from "vue";

const props = defineProps({
  value: String,
});
const copy = () => {
  modernCopy(props.value);
  notification.success(`${props.value} copied to clipboard!`);
};
</script>

<template>
  <code>
    {{ value }}
  </code>
  <code
    @click="copy"
    class="has-background-dark clickable has-tooltip-right"
    data-tooltip="Copy to clipboard"
  >
    <i class="fas fa-clipboard-list"></i>
  </code>
</template>

<style></style>
