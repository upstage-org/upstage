<template>
  <Logo id="live-logo" />
  <div id="main-content">
    <PageLoader v-if="loading" />
    <template v-else>
      <router-view />
      <LoginPrompt />
    </template>
  </div>
</template>

<script>
import Logo from "@/components/Logo";
import PageLoader from "./PageLoader.vue";
import LoginPrompt from "./LoginPrompt";
import { useStore } from "vuex";
import { computed } from "vue";
export default {
  components: { Logo, PageLoader, LoginPrompt },
  setup: () => {
    const store = useStore();
    const loading = computed(() => store.state.stage.preloading);
    return {
      loading,
    };
  },
};
</script>

<style>
#main-content {
  min-height: calc(100vh - 120px);
}
#live-logo {
  position: fixed;
  right: 10px;
  z-index: 100;
}
</style>