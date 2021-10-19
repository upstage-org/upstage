<script setup lang="ts">
import MediaFilter from './components/media/MediaFilter.vue';
import MediaTable from './components/media/MediaTable.vue';
</script>

<template>
  <a-layout class="pb-4">
    <MediaFilter />
    <MediaTable />
  </a-layout>
</template>
