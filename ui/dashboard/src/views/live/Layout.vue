<template>
  <Logo id="live-logo" />
  <div id="main-content">
    <PageLoader v-if="loading" />
    <router-view v-else />
  </div>
</template>

<script>
import Logo from "@/components/Logo";
import PageLoader from "./PageLoader.vue";
import { useStore } from "vuex";
import { computed } from 'vue';
export default {
  components: { Logo, PageLoader },
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