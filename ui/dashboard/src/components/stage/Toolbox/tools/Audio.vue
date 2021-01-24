<template>
  <div
    v-for="audio in audios"
    :key="audio"
    class="has-text-centered"
    @click="toggleAudio(audio)"
  >
    <div class="icon is-large" v-if="audio.isPlaying">
      <i class="fas fa-pause fa-2x"></i>
    </div>
    <div class="icon is-large" v-else>
      <i class="fas fa-play fa-2x"></i>
    </div>
    <div class="audio-name tag is-light is-block" :title="audio.file">
      {{ audio.name }}
    </div>
  </div>
</template>

<script>
import { useStore } from "vuex";

export default {
  setup: () => {
    const store = useStore();
    const audios = store.getters["stage/audios"];
    const playAudio = (audio) => {
      if (!audio.isPlaying) {
        store.dispatch("stage/playAudio", audio);
      }
    };
    const pauseAudio = (audio) => {
      store.dispatch("stage/pauseAudio", audio);
    };
    const toggleAudio = (audio) => {
      if (audio.isPlaying) {
        pauseAudio(audio);
      } else {
        playAudio(audio);
      }
    };
    return { audios, toggleAudio };
  },
};
</script>

<style scoped lang="scss">
@import "@/styles/mixins.scss";
.audio-name {
  font-weight: bold;
  font-size: 0.8rem;
  text-transform: capitalize;
  width: 100%;
  overflow-x: hidden;
  text-overflow: ellipsis;
}
.fas.fa-play {
  @include gradientText(#0052d4, #a5fecb);
}
.fas.fa-pause {
  @include gradientText(#ffb347, #a83279);
}
</style>