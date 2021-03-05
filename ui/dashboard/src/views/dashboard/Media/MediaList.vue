<template>
  <div class="columns is-multiline">
    <div class="column" v-for="media in mediaList" :key="media">
      <div class="">
        <div class="card-image">
          <figure class="image is-4by3">
            <img :src="'/' + media.fileLocation" />
          </figure>
        </div>
        <header class="card-header">
          <p class="card-header-title">{{ media.name }}</p>
        </header>
      </div>
    </div>
  </div>
</template>

<script>
import { inject } from "@vue/runtime-core";

export default {
  setup: () => {
    const mediaList = inject("mediaList");
    return { mediaList };
  },
};
</script>

<style>
</style>