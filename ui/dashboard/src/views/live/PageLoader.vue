<template>
  <section class="hero is-primary is-fullheight">
    <div class="hero-body">
      <div class="container">
        <h1 class="title">
          <button class="button is-primary is-loading is-large" />
          <span style="line-height: 1.75">Demo Stage</span>
        </h1>
        <h2 class="subtitle">
          Preloading avatars, props and backdrops...
          {{ progress }}/{{ preloadableAssets.length }}
        </h2>
        <div id="preloading-area">
          <img
            v-for="src in preloadableAssets"
            :key="src"
            :src="src"
            @load="increaseProgress"
          />
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { computed, ref } from "vue";
import { useStore } from "vuex";
export default {
  setup: () => {
    const store = useStore();
    const preloadableAssets = computed(
      () => store.getters["stage/preloadableAssets"]
    );
    const progress = ref(0);
    const stopLoading = () =>
      store.commit("stage/SET_PRELOADING_STATUS", false);
    const increaseProgress = () => {
      progress.value++;
      if (progress.value === preloadableAssets.value.length) {
        stopLoading();
      }
    };

    setTimeout(stopLoading, 60000);

    return { preloadableAssets, progress, increaseProgress };
  },
};
</script>

<style scoped lang="scss">
#preloading-area {
  width: 0px;
  height: 0px;
  overflow: hidden;
}
</style>