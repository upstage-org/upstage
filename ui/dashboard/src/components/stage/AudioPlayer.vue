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
import { computed, onMounted, watch } from "vue";
import { useStore } from "vuex";
import anime from "animejs";
export default {
  setup: () => {
    const store = useStore();
    const stopAudio = (audio) => {
      store.dispatch("stage/updateAudioStatus", {
        ...audio,
        isPlaying: false,
        currentTime: 0,
      });
    };
    const audios = store.getters["stage/audios"];
    let refs = [];
    const setRef = (el) => {
      const index = refs.length;
      refs.push(el);
      if (el) {
        el.addEventListener("ended", function () {
          const audio = audios[refs.indexOf(el)];
          if (audio.loop) {
            el.currentTime = 0;
            el.play();
          } else {
            stopAudio(audios[refs.indexOf(el)]);
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

    const fadeVolume = (audio, volume) => {
      anime({
        targets: audio,
        volume: volume,
        easing: "linear",
      });
    };

    const speed = computed(() => {
      if (store.state.stage.replay.isReplaying) {
        return Math.min(store.state.stage.replay.speed, 8);
      }
      return 1;
    });

    const handleAudioChange = () => {
      audios.forEach((audio, i) => {
        if (audio.changed) {
          if (audio.isPlaying) {
            refs[i].playbackRate = speed.value;
            refs[i].play();
          } else {
            refs[i].pause();
          }
          if (audio.saken) {
            refs[i].currentTime = audio.currentTime ?? 0;
          }
          fadeVolume(refs[i], audio.volume ?? 1);
          audio.changed = false;
          audio.saken = false;
        }
      });
    };

    watch(audios, handleAudioChange);
    onMounted(handleAudioChange);

    return { audios, setRef };
  },
};
</script>

<style scoped>
audio {
  display: none;
}
</style>