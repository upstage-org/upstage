<template>
  <section class="hero is-fullheight">
    <div class="hero-body">
      <div class="container">
        <h1 class="title" v-if="model">
          {{ model.name }}
        </h1>
        <h1 class="title" v-else-if="preloadableAssets.length">Demo Stage</h1>
        <h2 class="subtitle">
          <button class="button is-primary is-loading" />
          <span style="line-height: 2">
            <span v-if="preloadableAssets.length">
              Preloading avatars, props and backdrops...
              {{ progress }}/{{ preloadableAssets.length }}
            </span>
            <span v-else>Loading stage information...</span>
          </span>
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
    const model = computed(() => store.state.stage.model);
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

    return { model, preloadableAssets, progress, increaseProgress };
  },
};
</script>

<style scoped lang="scss">
#preloading-area {
  width: 0px;
  height: 0px;
  overflow: hidden;
}
section {
  background-color: #30ac45;
  * {
    color: white;
    background-color: transparent !important;
  }
}
</style>