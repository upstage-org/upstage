<template>
  <div v-for="stream in streams" :key="stream">
    <Skeleton :data="stream">
      <template v-if="stream.isRTMP">
        <div class="centered">
          <RTMPStream v-if="stream.alive" :src="stream.url"></RTMPStream>
          <QRCodePopup v-else :stream="stream" />
        </div>
      </template>
      <video v-else :src="stream.url"></video>
    </Skeleton>
  </div>
  <div v-if="loading">
    <Loading height="64px" />
  </div>
  <div v-else @click="fetchRunningStreams">
    <div class="icon is-large">
      <Icon src="refresh.svg" size="36" />
    </div>
    <span class="tag is-light is-block">Refresh</span>
  </div>
</template>

<script>
import { computed, onMounted } from "vue";
import { useStore } from "vuex";
import Skeleton from "../../Skeleton";
import QRCodePopup from "./QRCodePopup";
import Icon from "@/components/Icon";
import RTMPStream from "@/components/RTMPStream";
import Loading from "@/components/Loading";

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
    const runningStreams = computed(() => store.state.stage.runningStreams);
    const loading = computed(() => store.state.stage.loadingRunningStreams);
    const fetchRunningStreams = () => {
      store.dispatch("stage/getRunningStreams");
    };

    const autoDetect = computed(
      () => store.state.stage.config.streaming?.autoDetect
    );
    onMounted(() => {
      fetchRunningStreams();
    });

    const streams = computed(() => {
      const res = [...store.state.stage.tools.streams];
      res.forEach((s) => (s.alive = false));
      runningStreams.value.forEach((stream) => {
        const index = res.findIndex((s) => s.url === stream.url);
        if (index >= 0) {
          res[index].alive = true;
          res[index].w = stream.w
          res[index].h = stream.h
        } else {
          if (autoDetect.value) {
            res.push(stream);
          }
        }
      });
      console.log(res)
      return res;
    });

    return { streams, loading, fetchRunningStreams, autoDetect };
  },
};
</script>

<style lang="scss" scoped>
@import "@/styles/mixins.scss";
.fas.fa-plus {
  @include gradientText(#30ac45, #6fb1fc);
}
video {
  height: 100%;
}
.centered {
  margin: auto;
}
</style>