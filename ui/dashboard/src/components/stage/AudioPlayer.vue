<template>
  <audio v-for="audio in audios" :key="audio" :ref="setRef" preload="auto">
    <source :src="audio.src" type="audio/mpeg" />
    <source :src="audio.src" type="audio/ogg" />
    <source :src="audio.src" type="audio/wav" />
    <source :src="audio.src" type="audio/x-aiff" />
    <object>
      <param name="src" :value="audio.src" />
      <param name="controller" value="false" />
      <embed :src="audio.src" controller="false" type="audio/mpeg" />
    </object>
  </audio>
</template>

<script>
import { watch } from "vue";
import { useStore } from "vuex";
export default {
  setup: () => {
    const store = useStore();
    const audios = store.getters["stage/audios"];
    let refs = [];
    const setRef = (el) => {
      refs.push(el);
    };
    watch(audios, () => {
      audios.forEach((audio, i) => {
        if (audio.isPlaying) {
          refs[i].play();
        } else {
          refs[i].pause();
        }
      });
    });

    return { audios, setRef };
  },
};
</script>

<style scoped>
audio {
  display: none;
}
</style>