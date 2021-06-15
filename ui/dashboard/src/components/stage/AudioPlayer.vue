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
    const pauseAudio = (audio) => {
      store.dispatch("stage/updateAudioStatus", { ...audio, isPlaying: false });
    };
    const audios = store.getters["stage/audios"];
    let refs = [];
    const setRef = (el) => {
      const index = refs.length;
      refs.push(el);
      if (el) {
        el.addEventListener("ended", function () {
          const audio = audios[refs.indexOf(el)];
          console.log(audio.loop);
          if (audio.loop) {
            el.currentTime = 0;
            el.play();
          } else {
            pauseAudio(audios[refs.indexOf(el)]);
          }
        });
        el.addEventListener("loadedmetadata", function () {
          store.commit("stage/UPDATE_AUDIO_PLAYER_STATUS", {
            index,
            duration: el.duration,
          });
        });
        el.addEventListener("timeupdate", function () {
          store.commit("stage/UPDATE_AUDIO_PLAYER_STATUS", {
            index,
            currentTime: el.currentTime,
          });
        });
      }
    };
    watch(audios, () => {
      audios.forEach((audio, i) => {
        if (audio.changed) {
          refs[i].currentTime = audio.currentTime ?? 0;
          refs[i].volume = audio.volume ?? 1;
          if (audio.isPlaying) {
            refs[i].play();
          } else {
            refs[i].pause();
          }
          if (audio.currentTime) {
            refs[i].currentTime = audio.currentTime;
          }
          audio.changed = false;
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