<template>
  <div
    v-for="(audio, i) in audios"
    :key="audio"
    class="audio has-text-centered"
    :class="{ 'is-playing': audio.isPlaying }"
  >
    <ContextMenu>
      <template #trigger>
        <template v-if="audio.isPlaying">
          <div class="icon is-large" @click="togglePlaying(audio)">
            <Icon size="36" src="pause.svg" />
          </div>
          <input
            class="slider is-fullwidth is-primary mt-0"
            min="0"
            :max="audioPlayers[i]?.duration"
            :value="audioPlayers[i]?.currentTime ?? 0"
            @change="seek(audio, $event)"
            type="range"
          />
          <span v-if="i < 10" class="wattermark">{{ i + 1 }}</span>
        </template>
        <div v-else @click="togglePlaying(audio)">
          <div class="icon is-large">
            <Icon size="36" src="play.svg" />
          </div>
          <span class="audio-name tag is-light is-block" :title="audio.file">
            {{ audio.name }}
          </span>
          <span v-if="i < 10" class="wattermark">{{ i + 1 }}</span>
        </div>
      </template>
      <template #context>
        <div class="field has-addons menu-group px-4 my-2">
          <p class="control menu-group-title">
            <span class="panel-icon pt-1">
              <Icon src="loop.svg" />
            </span>
          </p>
          <p class="control menu-group-item">
            <Switch
              :modelValue="audio.loop"
              @update:modelValue="
                toggleLoop(audio, $event, audioPlayers[i]?.currentTime)
              "
            />
          </p>
        </div>
        <div class="field has-addons menu-group px-4 my-2">
          <p class="control menu-group-title">
            <span class="panel-icon pt-1">
              <Icon src="voice-setting.svg" />
            </span>
          </p>
          <p class="control menu-group-item">
            <input
              class="slider is-fullwidth is-primary my-0"
              step="0.01"
              min="0"
              max="1"
              :value="audio.volume ?? 1"
              @change="setVolume(audio, $event, audioPlayers[i]?.currentTime)"
              type="range"
            />
          </p>
        </div>
      </template>
    </ContextMenu>
  </div>
</template>

<script>
import { useStore } from "vuex";
import Icon from "@/components/Icon";
import ContextMenu from "@/components/ContextMenu";
import Switch from "@/components/form/Switch";
import { computed } from "@vue/runtime-core";
import { useShortcut } from "../../composable";

export default {
  components: { Icon, ContextMenu, Switch },
  setup: () => {
    const store = useStore();
    const audios = computed(() => store.getters["stage/audios"]);
    const audioPlayers = computed(() => store.state.stage.audioPlayers);

    const togglePlaying = (audio) => {
      audio.isPlaying = !audio.isPlaying;
      audio.currentTime = 0;
      store.dispatch("stage/updateAudioStatus", audio);
    };
    const toggleLoop = (audio, loop, currentTime) => {
      audio.loop = loop;
      audio.currentTime = currentTime;
      store.dispatch("stage/updateAudioStatus", audio);
    };
    const seek = (audio, e) => {
      audio.currentTime = e.target.value;
      store.dispatch("stage/updateAudioStatus", audio);
    };
    const setVolume = (audio, e, currentTime) => {
      audio.volume = e.target.value;
      audio.currentTime = currentTime;
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

    return { audios, togglePlaying, toggleLoop, setVolume, audioPlayers, seek };
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
.audio.is-playing {
  width: 200px !important;
}
.wattermark {
  position: absolute;
  top: 0;
  transform: translateX(-50%);
  opacity: 0.5;
}
</style>