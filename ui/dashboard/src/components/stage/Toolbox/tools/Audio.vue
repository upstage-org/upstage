<template>
  <div
    v-for="(audio, i) in audios"
    :key="audio"
    class="audio has-text-centered"
    :class="{ 'is-playing': audio.isPlaying }"
    @mouseenter="i > audios.length - 3 ? scrollToEnd() : null"
  >
    <div class="audio-name">
      <span v-if="i < 10">{{ i + 1 }}.</span>
      <span :title="audio.file">{{ audio.name }}</span>
    </div>
    <div class="buttons">
      <template v-if="audio.isPlaying">
        <div class="icon" @click="togglePlaying(audio, audioPlayers[i]?.currentTime)">
          <Icon size="24" src="pause.svg" />
        </div>
        <div class="icon" @click="stopAudio(audio)">
          <Icon size="24" src="clear.svg" />
        </div>
      </template>
      <template v-else>
        <div class="icon play-button" @click="togglePlaying(audio, audioPlayers[i]?.currentTime)">
          <Icon size="24" src="play.svg" />
        </div>
      </template>
      <div
        class="icon"
        :class="{ grayscale: !audio.loop }"
        @click="toggleLoop(audio, audioPlayers[i]?.currentTime)"
      >
        <Icon size="24" src="loop.svg" />
      </div>
    </div>
    <div class="sliders">
      <div class="addon volume">
        <div
          class="icon"
          :class="{ grayscale: !showVolumeSlider }"
          @click="showVolumeSlider = !showVolumeSlider"
        >
          <Icon size="24" src="voice-setting.svg" />
        </div>
        <input
          v-if="showVolumeSlider"
          class="slider is-fullwidth is-dark my-0"
          step="0.01"
          min="0"
          max="1"
          :value="audio.volume ?? 1"
          @change="setVolume(audio, $event, audioPlayers[i]?.currentTime)"
          type="range"
        />
      </div>
      <input
        class="slider is-fullwidth is-primary mt-0"
        min="0"
        :max="audioPlayers[i]?.duration"
        :value="audioPlayers[i]?.currentTime ?? 0"
        @change="seek(audio, $event)"
        type="range"
      />
      <div class="addon">
        <span v-if="audio.isPlaying">{{ displayTimestamp(audioPlayers[i]?.currentTime ?? 0) }}</span>
        <span v-else>{{ displayTimestamp(audioPlayers[i]?.duration) }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { useStore } from "vuex";
import Icon from "@/components/Icon";
import { computed, ref } from "@vue/runtime-core";
import { useShortcut } from "../../composable";
import { displayTimestamp } from "@/utils/common";
import anime from "animejs";

export default {
  components: { Icon },
  setup: () => {
    const store = useStore();
    const audios = computed(() => store.getters["stage/audios"]);
    const audioPlayers = computed(() => store.state.stage.audioPlayers);

    const togglePlaying = (audio, currentTime) => {
      audio.isPlaying = !audio.isPlaying;
      audio.currentTime = currentTime;
      audio.saken = true;
      store.dispatch("stage/updateAudioStatus", audio);
    };
    const stopAudio = (audio) => {
      audio.currentTime = 0;
      audio.saken = true;
      audio.isPlaying = false;
      store.dispatch("stage/updateAudioStatus", audio);
    };
    const toggleLoop = (audio, currentTime) => {
      audio.loop = !audio.loop;
      audio.currentTime = currentTime;
      store.dispatch("stage/updateAudioStatus", audio);
    };
    const seek = (audio, e) => {
      audio.currentTime = e.target.value;
      audio.saken = true;
      store.dispatch("stage/updateAudioStatus", audio);
    };
    const setVolume = (audio, e) => {
      audio.volume = e.target.value;
      store.dispatch("stage/updateAudioStatus", audio);
    };

    useShortcut((e) => {
      if (isFinite(e.key)) {
        const i = e.key - 1;
        if (audios.value.length > i && i >= 0) {
          togglePlaying(audios.value[i]);
        }
      }
    });
    const showVolumeSlider = ref(false)
    const scrollToEnd = () => {
      const topbar = document.querySelector('#topbar')
      if (topbar) {
        anime({
          targets: topbar,
          scrollLeft: topbar.scrollWidth,
          easing: "easeInOutQuad",
        });
      }
    };

    return {
      audios,
      togglePlaying,
      stopAudio,
      toggleLoop,
      setVolume,
      audioPlayers,
      seek,
      displayTimestamp,
      showVolumeSlider,
      scrollToEnd
    };
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
.audio {
  transition-duration: 0.25s;
  overflow-y: hidden;
  margin-top: -6px;
  height: 86px !important;

  .buttons {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 0;
    height: 32px;

    .play-button {
      height: 36px;
      img {
        height: 48px !important;
      }
    }

    > * {
      margin: 4px 8px;
      display: none;
      &:first-child {
        display: block;
      }
    }
  }
  .sliders {
    display: none !important;
    margin-bottom: 0;
    height: 16px;
    .slider {
      margin: 0 4px;
    }
    .volume {
      .slider {
        position: absolute;
        top: 8px;
        left: 15px;
        width: 100px;
        transform: scale(0.5) rotate(270deg) translateX(-100%);
        transform-origin: left top;
      }
    }
  }
  &.is-playing {
    .sliders {
      display: flex !important;
      .addon {
        display: none;
      }
    }
  }
  &:hover {
    width: 250px !important;
    .sliders {
      display: flex !important;
      .addon {
        display: block;
      }
    }
    .buttons {
      > * {
        display: block;
      }
      .play-button {
        height: 32px;
        img {
          height: 24px !important;
        }
      }
    }
  }
}
.grayscale {
  filter: grayscale(1);
}
</style>