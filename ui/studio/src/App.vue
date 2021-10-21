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
    <a-layout class="pb-4 backdrop">
      <MediaFilter />
      <MediaTable />
    </a-layout>
  </Authorized>
</template>

<style>
.backdrop {
  background-image: url(https://dev-app1.upstage.org.nz/V4.0/static/assets/curtain/dd4820dd9f604decbb3eda08435edf6f.jpg?t=1627393687);
}
</style>