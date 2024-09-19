<template>
  <div>
    <Object :object="stream">
      <template #menu="slotProps">
        <div class="field has-addons menu-group">
          <b class="m-2">{{ $t("shape") }}</b>
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
        <template v-if="object.isRTMP">
          <a v-if="object.type === 'stream'" class="panel-block" @click="refreshStreams">
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
        </template>
        <template v-else>
          <template v-if="!stream.jitsi">
            <a v-if="stream.isPlaying" class="panel-block" @click="pauseStream(slotProps)">
              <span class="panel-icon">
                <i class="fas fa-pause"></i>
              </span>
              <span>{{ $t("pause") }}</span>
            </a>
            <a v-else class="panel-block" @click="playStream(slotProps)">
              <span class="panel-icon">
                <i class="fas fa-play"></i>
              </span>
              <span>{{ $t("play") }}</span>
            </a>
            <a v-if="object.type === 'stream'" class="panel-block" @click="restartVideo">
              <span class="panel-icon">
                <i class="fas fa-sync"></i>
              </span>
              <span>{{ $t("restart") }}</span>
            </a>
          </template>
          <a v-if="!stream.jitsi" class="panel-block" @click="toggleLoop">
            <span class="panel-icon">
              <i v-if="stream.loop" class="fas fa-infinity"></i>
              <b v-else>1</b>
            </span>
            <span v-if="stream.loop">{{ $t("loop.on") }}</span>
            <span v-else>{{ $t("loop.off") }}</span>
          </a>
        </template>

        <MenuContent :object="object" :stream="stream" v-bind="slotProps" v-model:active="active" />
      </template>

      <template #render>
        <Loading v-if="loading" height="100%" />
        <div v-if="stream.jitsi" id="meeting-room" class="frame" :class="activeMovable ? 'disable-pointer' : ''">
          <div :style="{
            'height': '100%',
            'overflow': 'hidden',
            'border-radius': stream.shape === 'circle' ? '100%' : 0,
          }">
            <div class="room" ref="room"></div>
          </div>
        </div>
        <template v-else>
          <video v-bind:id="'video' + stream.id" v-show="!loading" ref="video" :src="object.url" :muted="localMuted"
            preload="auto" disablepictureinpicture @loadeddata="loadeddata" @ended="stream.isPlaying = false" :style="{
              'border-radius': stream.shape === 'circle' ? '100%' : 0,
            }" :loop="stream.loop"></video>
          <button v-if="isPlayer" class="button is-small mute-icon clickable" @mousedown="toggleMuted">
            <i v-if="localMuted" class="fas fa-volume-mute has-text-danger"></i>
            <i v-else class="fas fa-volume-up has-text-primary"></i>
          </button>
        </template>
      </template>
    </Object>
  </div>
</template>

<script>
import flvjs from "flv.js";
import { computed, reactive, ref, watch, onMounted } from "vue";
import Object from "../Object.vue";
import { useStore } from "vuex";
import { useFlv, useCatchup } from "./composable";
import { getSubsribeLink } from "utils/streaming";
import Loading from "components/Loading.vue";
import MenuContent from "../Avatar/ContextMenu.vue";
import { useJitsiDomain } from "../Meeting/composable";

export default {
  components: { Object, Loading, MenuContent },
  emits: ["update:active", "hold"],
  props: ["object", "setSliderMode"],
  setup: (props) => {
    const store = useStore();
    const shapes = computed(() => store.state.stage.tools.shapes);
    const loading = ref(!props.object.jitsi);
    const stream = reactive({
      ...props.object,
      isPlaying: props.object.isRTMP ? true : props.object.isPlaying,
      src: loading,
    });
    const video = ref();
    const room = ref();
    const isPlayer = computed(() => store.getters["stage/canPlay"]);

    const synchronize = () => {
      if (stream.isPlaying && video.value) {
        video.value.play();
      } else {
        video.value.pause();
      }
    };
    onMounted(() => {
      const domain = useJitsiDomain();
      const options = {
        roomName: stream.name,
        subject: "Powered by Jitsi",
        width: "100%",
        height: "100%",
        parentNode: room.value,
        userInfo: {
          email: store.state.user.user?.email,
          displayName: store.getters["user/chatname"],
        },
        configOverwrite: {
          prejoinConfig: { enabled: false },
          disableRemoteMute: true,
          notifications: [],
          hideParticipantsStats: true,
          disableSelfViewSettings: true,
          remoteVideoMenu: {
            disabled: true
          },
          connectionIndicators: {
            disabled: true
          },
          ...stream.description != store.state.user.user?.email ? {
            filmstrip: { disabled: true },
            participantsPane: { enabled: false },
            toolbarButtons: [],
            disableTileView: true,
            startWithAudioMuted: true,
            startWithVideoMuted: true
          } : {
            toolbarButtons: ['microphone', 'camera', 'tileview']
          }
        },
        interfaceConfigOverwrite: { SHOW_CHROME_EXTENSION_BANNER: false },
        disableInitialGUM: true,
      };
      const api = new window.JitsiMeetExternalAPI(domain, options);
      console.log("***********", api);
    });
    watch(
      () => stream.replayed,
      () => {
        video.value.currentTime = 0;
      },
    );

    watch(
      () => props.object,
      () => {
        window.Object.assign(stream, props.object);
        if (props.object.jitsi) return;
        synchronize();
      },
    );
    const loadeddata = () => {
      if (props.object.jitsi) return;
      loading.value = false;
      synchronize();
    };

    if (props.object.isRTMP) {
      const fullUrl = computed(() => getSubsribeLink(props.object.url));
      useCatchup(video);
      useFlv(video, fullUrl);
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

    const refreshStreams = () => {
      if (props.object.jitsi) return;
      let video = document.getElementById("video" + props.stream.id);
      if (stream.isPlaying && video) {
        const fullUrl = computed(() => getSubsribeLink("your_stream_key"));

        if (flvjs.isSupported()) {
          const flvPlayer = flvjs.createPlayer({
            type: "flv",
            url: fullUrl.value + "?" + new Date(),
          });
          flvPlayer.attachMediaElement(video);
          flvPlayer.load();
          flvPlayer.play();
        }

        video.play();
      } else {
        video.pause();
      }
    };

    const playStream = () => {
      store
        .dispatch("stage/shapeObject", {
          ...stream,
          isPlaying: true,
        })
        .then(props.closeMenu);
    };

    const restartVideo = () => {
      store
        .dispatch("stage/shapeObject", {
          ...stream,
          replayed: stream.replayed + 1,
        })
        .then(props.closeMenu);
    };

    const toggleLoop = () => {
      store
        .dispatch("stage/shapeObject", {
          ...stream,
          loop: !stream.loop,
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
    const activeMovable = computed(() => store.getters["stage/activeMovable"]);

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
      refreshStreams,
      openVolumePopup,
      restartVideo,
      toggleLoop,
      room,
      activeMovable
    };
  },
};
</script>

<style lang="scss" scoped>
.panel-block {
  font-size: 14px;
}

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

.frame {
  border: 2px solid black;
  border-top: 10px solid #007011;
  border-radius: 8px;
  box-sizing: border-box;
  overflow: hidden;
  height: 100%;

  .room {
    height: 100%;
  }
}

.disable-pointer {
  pointer-events: none;
}
</style>
