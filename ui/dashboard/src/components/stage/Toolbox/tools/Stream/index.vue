<template>
  <div @click="newStream">
    <div class="icon is-large">
      <Icon src="new.svg" size="36" />
    </div>
    <span class="tag is-light is-block">New</span>
  </div>
  <div>
    <Webcam />
  </div>
  <div v-for="stream in streams" :key="stream">
    <Skeleton :data="stream">
      <RTMPStream v-if="stream.isRTMP" :src="stream.url"></RTMPStream>
      <video v-else :src="stream.url"></video>
    </Skeleton>
  </div>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import Skeleton from "../../Skeleton";
import Icon from "@/components/Icon";
import RTMPStream from "@/components/RTMPStream";
import Webcam from "./Webcam";

export default {
  components: { Skeleton, Icon, Webcam, RTMPStream },
  setup: () => {
    const store = useStore();
    const newStream = () => {
      store.dispatch("stage/openSettingPopup", {
        type: "CreateStream",
      });
    };
    const streams = computed(() => store.state.stage.tools.streams);

    return { streams, newStream, Webcam };
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