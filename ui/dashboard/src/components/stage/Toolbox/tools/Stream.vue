<template>
  <div @click="newStream">
    <div class="icon is-large">
      <i class="fas fa-plus fa-2x"></i>
    </div>
    <span class="tag is-light is-block">New</span>
  </div>
</template>

<script>
import { useStore } from "vuex";
export default {
  setup: () => {
    const store = useStore();
    const newStream = () => {
      store.dispatch("stage/openSettingPopup", {
        type: "CreateStream",
      });
    };

    return { newStream };
  },
};
</script>

<style lang="scss" scoped>
@import "@/styles/mixins.scss";
.fas.fa-plus {
  @include gradientText(#30ac45, #6fb1fc);
}
</style>