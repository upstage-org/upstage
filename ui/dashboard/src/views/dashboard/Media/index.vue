<template>
  <section class="hero is-small is-light is-bold">
    <div class="hero-body">
      <h1 class="title is-inline">Media</h1>
      &nbsp;
      <MediaUpload />
    </div>
  </section>
  <div class="columns">
    <div class="column is-4">
      <aside class="menu box has-background-light mx-4">
        <ul class="menu-list">
          <li>
            <a class="is-active">My Media</a>
          </li>
          <li>
            <a>Backdrops</a>
          </li>
          <li>
            <a>Avatars</a>
          </li>
          <li>
            <a>Props</a>
          </li>
          <li>
            <a>Audio</a>
          </li>
          <li>
            <a>Stream</a>
          </li>
        </ul>
      </aside>
    </div>
    <div class="column is-8">
      <div class="pt-4 pr-4 pb-4">
        <MediaList />
      </div>
    </div>
  </div>
</template>

<script setup>
import MediaList from "./MediaList";
import MediaUpload from "@/components/MediaUpload";
</script>

<style>
</style>