<script setup lang="ts">
import MediaFilter from './components/media/MediaFilter.vue';
import MediaTable from './components/media/MediaTable.vue';
import Authorized from './components/Authorized.vue';
import { provide } from '@vue/runtime-core';
import { DefaultApolloClient } from '@vue/apollo-composable'
import { apolloClient } from './apollo';
import Dropzone from './components/media/Dropzone.vue';
import MediaUpload from './components/media/MediaForm/index.vue';

provide(DefaultApolloClient, apolloClient)
</script>

<template>
  <Authorized>
    <a-layout class="pb-4 layout">
      <Dropzone>
        <MediaFilter />
        <MediaTable />
        <MediaUpload />
      </Dropzone>
    </a-layout>
  </Authorized>
</template>

<style>
.layout {
  min-height: 100vh;
}
</style>