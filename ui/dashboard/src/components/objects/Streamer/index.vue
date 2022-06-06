<template>
  <div>
    <Object :object="stream">
      <template #menu="slotProps">
        <div class="field has-addons menu-group">
          <p class="control menu-group-item">
            <button class="button is-light" @click="clip(null)">
              <div class="icon">
                <i class="fas fa-square"></i>
              </div>
            </button>
          </p>
          <p class="control menu-group-item" @click="clip('circle')">
            <button class="button is-light">
              <div class="icon">
                <i class="fas fa-circle"></i>
              </div>
            </button>
          </p>
        </div>
        <a v-if="stream.isPlaying" class="panel-block has-text-info" @click="pauseStream(slotProps)">
          <span class="panel-icon">
            <i class="fas fa-pause"></i>
          </span>
          <span>{{ $t("pause") }}</span>
        </a>
        <a v-else class="panel-block has-text-info" @click="playStream(slotProps)">
          <span class="panel-icon">
            <i class="fas fa-play"></i>
          </span>
          <span>{{ $t("play") }}</span>
        </a>
        <a v-if="object.type === 'stream'" class="panel-block has-text-info" @click="restartStream">
          <span class="panel-icon">
            <i class="fas fa-sync"></i>
          </span>
          <span>{{ $t("restart") }}</span>
        </a>
        <a class="panel-block" @click="openVolumePopup(slotProps)">
          <span class="panel-icon">
            <Icon src="voice-setting.svg" />
          </span>
          <span>{{ $t("volumn_setting") }}</span>
        </a>

        <MenuContent :object="object" :stream="stream" v-bind="slotProps" v-model:active="active" />
      </template>

      <template #render>
        <Loading v-if="loading" height="100%" />
        <video v-bind:id="'video' + stream.id" v-show="!loading" ref="video" :src="object.url" :muted="localMuted"
          preload="auto" disablepictureinpicture @loadeddata="loadeddata" @ended="stream.isPlaying = false" :style="{
            'border-radius': stream.shape === 'circle' ? '100%' : 0,
          }"></video>
        <button v-if="isPlayer" class="button is-small mute-icon clickable" @mousedown="toggleMuted">
          <i v-if="localMuted" class="fas fa-volume-mute has-text-danger"></i>
          <i v-else class="fas fa-volume-up has-text-primary"></i>
        </button>
      </template>
    </Object>
  </div>
</template>

<script>
import flvjs from "flv.js";
import { computed, reactive, ref, watch } from "vue";
import Object from "../Object.vue";
import { useStore } from "vuex";
import { useFlv, useCatchup } from "./composable";
import { getSubsribeLink } from "@/utils/streaming";
import Loading from "@/components/Loading.vue";
import MenuContent from '../Avatar/ContextMenu'

export default {
  components: { Object, Loading, MenuContent },
  emits: ["update:active", "hold"],
  props: ["object", "setSliderMode",],
  setup: (props) => {
    const store = useStore();
    const shapes = computed(() => store.state.stage.tools.shapes);

    const stream = reactive({ ...props.object, isPlaying: true, src: loading });
    const video = ref();
    const isPlayer = computed(() => store.getters["stage/canPlay"]);

    const synchronize = () => {
      if (stream.isPlaying && video.value) {
        video.value.play();
      } else {
        video.value.pause();
      }
    };

    watch(
      () => props.object,
      () => {
        window.Object.assign(stream, props.object);
        synchronize();
      }
    );
    const loading = ref(true);
    const loadeddata = () => {
      loading.value = false;
      synchronize();
    };

    if (props.object.isRTMP) {
      const fullUrl = computed(() => getSubsribeLink(props.object.url));
      useCatchup(video);
      const { playable } = useFlv(video, fullUrl);

      watch(playable, value => {
        console.log("playable", value);
        if (!value) {
          store.dispatch("stage/deleteObject", props.object);
        }
      })
    }

    const clip = (shape) => {
      store.dispatch("stage/shapeObject", {
        ...stream,
        shape,
      });
    };

    const localMuted = ref(false);
    const toggleMuted = () => {
      localMuted.value = !localMuted.value;
    };
    const pauseStream = () => {
      store
        .dispatch("stage/shapeObject", {
          ...stream,
          isPlaying: false,
        })
        .then(props.closeMenu);
    };

    const restartStream = () => {
      store.dispatch("stage/getRunningStreams")
      let video = document.getElementById('video' + props.stream.id);
      if (stream.isPlaying && video) {
        const fullUrl = computed(() => getSubsribeLink('your_stream_key'));

        if (flvjs.isSupported()) {
          const flvPlayer = flvjs.createPlayer({
            type: "flv",
            url: fullUrl.value + "?" + new Date(),
          });
          flvPlayer.attachMediaElement(video);
          flvPlayer.load();
          flvPlayer.play();
        }

        video.play()
      } else {
        video.pause()
      }
    }

    const playStream = () => {
      store
        .dispatch("stage/shapeObject", {
          ...stream,
          isPlaying: true,
        })
        .then(props.closeMenu);
    };

    const openVolumePopup = () => {
      store
        .dispatch("stage/openSettingPopup", {
          type: "VolumeParameters",
        })
        .then(props.closeMenu);
    };

    return {
      video,
      stream,
      loadeddata,
      clip,
      shapes,
      loading,
      localMuted,
      toggleMuted,
      isPlayer,
      pauseStream,
      playStream,
      restartStream,
      openVolumePopup,
    };
  },
};
</script>

<style lang="scss" scoped>
.mute-icon {
  position: absolute;
  width: 24px;
  height: 20px;
  bottom: 8px;
  right: 8px;

  &:hover {
    transform: scale(1.2);
  }
}
</style>