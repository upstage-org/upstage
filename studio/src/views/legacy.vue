<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const iframeSrc = computed(() =>
  !route.params.path.includes(":") && !route.params.path.startsWith("/")
    ? `/${route.params.path}`
    : route.params.path
);
</script>

<template>
  <iframe v-if="iframeSrc" class="bg-gray-200" :src="iframeSrc" />
</template>

<style lang="less" scoped>
iframe {
  width: 100%;
  height: 100%;
  border-radius: 12px;
  border: none;
}
</style>
