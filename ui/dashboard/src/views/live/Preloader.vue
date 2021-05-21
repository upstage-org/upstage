<template>
  <transition @leave="leave">
    <section
      v-if="!ready || !clicked"
      class="hero is-fullheight is-fullwidth"
      :class="{ replaying }"
      @click="clicked = true"
    >
      <div class="hero-body">
        <div class="container">
          <template v-if="model">
            <h1 class="title" :class="{ 'mb-0': model.description }">
              {{ model.name }}
            </h1>
            <h2 v-if="model.description" class="subtittle">
              {{ model.description }}
            </h2>
            <h2 v-if="ready" class="subtitle">
              <span class="sparkle" style="line-height: 2">
                Stage loaded 100%, click anywhere to continue...
              </span>
            </h2>
            <h2 v-else class="subtitle">
              <button class="button is-primary is-loading" />
              <span style="line-height: 2">
                <span v-if="preloadableAssets.length">
                  Preloading avatars, props and backdrops...
                  {{ progress }}/{{ preloadableAssets.length }}

                  <div id="preloading-area">
                    <img
                      v-for="src in preloadableAssets"
                      :key="src"
                      :src="src"
                      @load="increaseProgress"
                    />
                  </div>
                </span>
              </span>
            </h2>
          </template>
          <template v-else-if="preloading">
            <h2 class="subtitle">
              <button class="button is-primary is-loading" />
              <span style="line-height: 2">Loading stage information...</span>
            </h2>
          </template>
          <template v-else>
            <h1 class="title">Stage not found!</h1>
            <span>Are you sure the stage url is correct 🤔?</span>
          </template>
        </div>
      </div>
    </section>
  </transition>
</template>

<script>
import { computed, inject, ref } from "vue";
import { useStore } from "vuex";
import anime from "animejs";
export default {
  setup: () => {
    const store = useStore();
    const preloading = computed(() => store.state.stage.preloading);
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

    const replaying = inject("replaying");
    const ready = computed(() => store.getters["stage/ready"]);
    const clicked = ref(false); // Trick the user to click in order to play meSpeak voice
    const leave = (el, complete) => {
      anime({
        targets: el,
        translateY: "-100%",
        easing: "easeOutBack",
        complete,
      });
    };

    return {
      model,
      preloadableAssets,
      progress,
      increaseProgress,
      preloading,
      replaying,
      ready,
      clicked,
      leave,
    };
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
  position: absolute;
  z-index: 20000;
  * {
    color: white;
    background-color: transparent !important;
  }
  &.replaying {
    background-color: #363636;
  }
}
.sparkle {
  animation: sparkle 1s infinite;
}
@keyframes sparkle {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
</style>