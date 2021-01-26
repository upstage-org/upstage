<template>
  <div v-if="stream.url" class="card-content">
    <div class="columns">
      <div class="column">
        <button v-if="stream.loading" class="button is-light is-loading is-fullwidth" style="height: 25vh">Loading</button>
        <video v-show="!stream.loading" preload="auto" controls :src="stream.url" @loadedmetadata="handleMetadata"></video>
      </div>
      <div class="column">
        <template  v-if="stream.metadata">
            <p>
                <ul>
                    <li>Duration: {{stream.metadata.duration}}</li>
                </ul>
            </p>
        </template>
        <p class="title">Change URL</p>
        <p>
            <input
                class="input"
                type="text"
                :placeholder="stream.url"
                @keyup.enter="(e) => (stream.url = e.target.value)"
            />
        </p>
      </div>
    </div>
  </div>
  <div v-else class="card-content">
    <p class="title">Enter stream url</p>
    <p>
      <input
        class="input"
        type="text"
        placeholder="https://www.w3schools.com/html/mov_bbb.mp4"
        @keyup.enter="(e) => (stream.url = e.target.value)"
      />
    </p>
    <p class="subtitle">{{ stream.url }}</p>
  </div>
  <footer class="card-footer" v-if="stream.url">
    <p class="card-footer-item has-background-primary has-text-white">
      <span> Put on Stage </span>
    </p>
    <p class="card-footer-item">
      <span class="has-text-primary"> Save </span>
    </p>
  </footer>
</template>

<script>
import { reactive } from "vue";
export default {
  setup: () => {
    const stream = reactive({
      loading: true,
    });

    const handleMetadata = (e) => {
      stream.loading = false;
      stream.metadata = e.target;
      console.log(stream.metadata);
    };

    return { stream, handleMetadata };
  },
};
</script>

<style>
.card-footer-item {
  cursor: pointer;
}
</style>