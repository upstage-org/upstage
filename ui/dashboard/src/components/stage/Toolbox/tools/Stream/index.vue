<template>
  <div @click="newStream">
    <div style="height: 48px">
      <OBSInstruction src="some_unique_key" />
    </div>
    <span class="tag is-light is-block">Instruction</span>
  </div>
  <div v-for="stream in streams" :key="stream">
    <Skeleton :data="stream">
      <RTMPStream v-if="stream.isRTMP" :src="stream.url"></RTMPStream>
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
import Icon from "@/components/Icon";
import RTMPStream from "@/components/RTMPStream";
import Loading from "@/components/Loading";
import OBSInstruction from "@/views/backstage/Media/OBSInstruction";

export default {
  components: { Skeleton, Icon, RTMPStream, Loading, OBSInstruction },
  setup: () => {
    const store = useStore();
    const streams = computed(() => store.state.stage.tools.streams);
    const loading = computed(() => store.state.stage.loadingRunningStreams);
    const fetchRunningStreams = () => {
      store.dispatch("stage/getRunningStreams");
    };
    onMounted(fetchRunningStreams);

    return { streams, loading, fetchRunningStreams };
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
</style>