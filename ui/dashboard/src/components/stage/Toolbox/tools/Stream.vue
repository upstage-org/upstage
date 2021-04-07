<template>
  <div @click="newStream">
    <div class="icon is-large">
      <Icon src="new.svg" size="36" />
    </div>
    <span class="tag is-light is-block">New</span>
  </div>
  <div v-for="stream in streams" :key="stream">
    <Skeleton :data="stream">
      <video :src="stream.url"></video>
    </Skeleton>
  </div>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import Skeleton from "@/components/objects/Skeleton";
import Icon from "@/components/Icon";

export default {
  components: { Skeleton, Icon },
  setup: () => {
    const store = useStore();
    const newStream = () => {
      store.dispatch("stage/openSettingPopup", {
        type: "CreateStream",
      });
    };
    const streams = computed(() => store.state.stage.tools.streams);

    return { streams, newStream };
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