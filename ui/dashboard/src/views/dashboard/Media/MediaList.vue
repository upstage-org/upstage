<template>
  <div class="columns">
    <div class="column is-3" v-for="media in mediaList" :key="media">
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

<script setup>
const { inject, watch } = require("@vue/runtime-core");

const mediaList = inject("mediaList");
</script>

<style>
</style>