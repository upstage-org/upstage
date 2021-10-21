<script setup lang="ts">
import MediaFilter from './components/media/MediaFilter.vue';
import MediaTable from './components/media/MediaTable.vue';
import Authorized from './components/Authorized.vue';
import { provide } from '@vue/runtime-core';
import { DefaultApolloClient } from '@vue/apollo-composable'
import { apolloClient } from './apollo';

provide(DefaultApolloClient, apolloClient)
</script>

<template>
  <Authorized>
    <a-layout class="pb-4">
      <MediaFilter />
      <MediaTable />
    </a-layout>
  </Authorized>
</template>

<style>
</style>