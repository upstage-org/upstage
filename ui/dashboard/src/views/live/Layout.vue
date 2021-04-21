<template>
  <Logo id="live-logo" />
  <div id="main-content">
    <Preloader />
    <template v-if="ready">
      <Live />
      <LoginPrompt />
      <SettingPopup />
    </template>
  </div>
</template>

<script>
import Logo from "@/components/Logo";
import SettingPopup from "@/components/stage/SettingPopup";
import Preloader from "./Preloader";
import LoginPrompt from "./LoginPrompt";
import Live from "./Live";
import { useStore } from "vuex";
import { computed } from "vue";
import { useRoute } from "vue-router";
export default {
  components: { Logo, Preloader, LoginPrompt, SettingPopup, Live },
  setup: () => {
    const store = useStore();
    const ready = computed(
      () => store.state.stage.model && !store.state.stage.preloading
    );

    const route = useRoute();
    store.dispatch("stage/loadStage", route.params.url);
    return {
      ready,
    };
  },
};
</script>

<style lang="scss">
#main-content {
  min-height: calc(100vh - 120px);
}
#live-logo {
  position: fixed;
  right: 0px;
  z-index: 1;
  max-width: 200px;

  @media screen and (min-width: 1024px) {
    img {
      max-height: unset;
    }
  }
}
</style>