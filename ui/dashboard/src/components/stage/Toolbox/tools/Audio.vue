<template>
  <div
    v-for="audio in audios"
    :key="audio"
    class="has-text-centered"
    @click="playAudio(audio)"
  >
    <div class="icon is-large">
      <i class="fas fa-play fa-2x"></i>
    </div>
    <div class="audio-name" :title="audio.file">{{ audio.name }}</div>
  </div>
</template>

<script>
import { useStore } from "vuex";

export default {
  components: {},
  setup: () => {
    const store = useStore();
    const audios = store.getters["stage/audios"];
    const playAudio = (audio) => {
      store.dispatch("stage/playAudio", audio);
    };
    return { audios, playAudio };
  },
};
</script>

<style scoped lang="scss">
.audio-name {
  font-weight: bold;
  font-size: 0.8rem;
  text-transform: capitalize;
  width: 100%;
  overflow-x: hidden;
  text-overflow: ellipsis;
}
</style>