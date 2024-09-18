<template>
  <div @click="createRoom" class="is-pulled-left room-skeleton">
    <div class="icon is-large">
      <Icon src="new.svg" size="36" />
    </div>
    <span class="tag is-light is-block">{{ $t("new_stream") }}</span>
  </div>
  <div v-for="stream in streams" :key="stream" :class="{ 'has-background-warning': !stream.ready && stream.alive }">
    <Skeleton :data="stream" :nodrop="stream.isRTMP && !stream.ready">
      <template v-if="stream.isRTMP">
        <div class="centered">
          <RTMPStream v-if="stream.alive" :src="stream.url" @scan="scanVideo($event, stream)"></RTMPStream>
          <QRCodePopup v-else :stream="stream" />
        </div>
      </template>
      <video v-else :src="stream.url"></video>
    </Skeleton>
  </div>
  <Skeleton v-for="(room, i) in rooms" :key="i" :data="room">
    <div class="room-skeleton">
      <Icon src="backdrop.svg" size="36" />
      <span class="tag is-light is-block">{{ room.name }}</span>
    </div>
  </Skeleton>
  <!-- <div v-if="loading">
    <Loading height="64px" />
  </div>
  <div v-else @click="fetchRunningStreams">
    <div class="icon is-large">
      <Icon src="refresh.svg" size="36" />
    </div>
    <span class="tag is-light is-block">{{ $t("refresh") }}</span>
  </div> -->
</template>

<script>
import { computed, onMounted } from "vue";
import { useStore } from "vuex";
import Skeleton from "../../Skeleton.vue";
import QRCodePopup from "./QRCodePopup.vue";
import Icon from "components/Icon.vue";
import RTMPStream from "components/RTMPStream.vue";
import Loading from "components/Loading.vue";

export default {
  components: {
    Skeleton,
    Icon,
    QRCodePopup,
    RTMPStream,
    Loading,
  },
  setup: () => {
    const store = useStore();
    const rooms = computed(() => store.state.stage.tools.streams.filter(el => el.jitsi));
    const runningStreams = computed(() => store.state.stage.runningStreams);
    const loading = computed(() => store.state.stage.loadingRunningStreams);
    const fetchRunningStreams = () => {

    };

    const autoDetect = computed(
      () => store.state.stage.config.streaming?.autoDetect,
    );
    onMounted(() => {
      //fetchRunningStreams();
    });

    const streams = computed(() => {
      const res = [...store.state.stage.tools.streams.filter(el => !el.jitsi)];
      res.forEach((s) => (s.alive = false));
      runningStreams.value.forEach((stream) => {
        const index = res.findIndex((s) => s.url === stream.url);
        if (index >= 0) {
          res[index].alive = true;
          if (stream.w > 0 && stream.h > 0) {
            res[index].w = stream.w;
            res[index].h = stream.h;
          }
        } else {
          if (autoDetect.value) {
            res.push(stream);
          }
        }
      });
      console.log(res);
      return res;
    });

    const scanVideo = ({ width, height }, stream) => {
      console.log(stream, width, height);
      if (!stream.ready) {
        Object.assign(stream, {
          w: (100 * width) / height,
          h: 100,
          ready: true,
        });
      }
    };

    const createRoom = () => {
      store.dispatch("stage/openSettingPopup", {
        type: "CreateStream",
      });
    };
    return { streams, loading, fetchRunningStreams, autoDetect, scanVideo, createRoom, rooms };
  },
};
</script>

<style lang="scss" scoped>
@mixin gradientText($from, $to) {
  background: linear-gradient(to top, $from, $to);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.fas.fa-plus {
  @include gradientText(#30ac45, #6fb1fc);
}

video {
  height: 100%;
}

.centered {
  margin: auto;
}

.pending-stream {
  cursor: not-allowed;
}

.room-skeleton {
  flex: none;
}

div:has(> .room-skeleton) {
  width: auto !important;
}
</style>
