<template>
  <div @click="newStream">
    <div class="icon is-large">
      <i class="fas fa-plus fa-2x"></i>
    </div>
    <span class="tag is-light is-block">New</span>
  </div>
  <div v-for="stream in streams" :key="stream">
    <Skeleton :data="stream" />
  </div>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import Skeleton from "@/components/objects/Skeleton";

export default {
  components: { Skeleton },
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
</style>