<template>
  <transition @leave="leave">
    <section
      v-if="!ready || !clicked"
      class="hero is-fullheight is-fullwidth cover-image"
      :class="{ replaying }"
      @click="clicked = true"
      :style="{
        'background-image': model && model.cover && `url(${model.cover})`,
        'background-color': backdropColor,
      }"
    >
      <div class="hero-body">
        <div class="container">
          <template v-if="model">
            <h1 class="title" :class="{ 'mb-0': model.description }">{{ model.name }}</h1>
            <h2 v-if="model.description" class="subtittle">{{ model.description }}</h2>
            <h2 v-if="ready" class="subtitle">
              <span
                class="sparkle"
                style="line-height: 2"
              >Stage loaded 100%, click anywhere to continue...</span>
            </h2>
            <h2 v-else class="subtitle">
              <template v-if="status !== 'live' && !canPlay">
                <span v-if="status" class="tag is-dark">{{ status.toUpperCase() }}</span>&nbsp;
                <span>This stage is not currently open to the public. Please come back later!</span>
              </template>
              <template v-else-if="preloadableAssets.length">
                <button class="button is-primary is-loading" />
                <span style="line-height: 2">
                  <span>
                    Preloading media...
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
              </template>
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
import { computed, inject, ref, watch, watchEffect, onUnmounted } from "vue";
import { useStore } from "vuex";
import anime from "animejs";
import { useAttribute } from "@/services/graphql/composable";
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
    watchEffect(() => {
      if (preloadableAssets.value.length === 0 && model.value) {
        stopLoading();
      }
    });

    watch(preloading, (val) => {
      const logo = document.querySelector('#live-logo')
      if (val) {
        logo.classList.add('preloader');
      } else {
        logo.classList.remove('preloader');
      }
    }, { immediate: true })

    const status = useAttribute(model, 'status')
    const timer = ref()
    watch(model, (val) => {
      if (val && status.value === 'live') {
        timer.value = setTimeout(stopLoading, 60000);
      }
    });
    onUnmounted(() => {
      if (timer.value) {
        clearInterval(timer.value)
      }
    })

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
    const backdropColor = computed(() => store.state.stage.backdropColor);

    const canPlay = computed(() => store.getters["stage/canPlay"]);

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
      backdropColor,
      status,
      canPlay
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
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
  text-shadow: black 0px 0px 3px;
  position: absolute;
  z-index: 20000;
  * {
    color: white;
  }
  button {
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