<template>
  <transition @enter="curtainEnter" @leave="curtainLeave">
    <img
      v-if="curtain"
      :key="curtain"
      :src="curtain"
      class="curtain"
      :style="{ opacity: canPlay ? 0.5 : 1 }"
    />
  </transition>
</template>

<script>
import { computed } from "@vue/runtime-core";
import anime from "animejs";
import { useStore } from "vuex";
export default {
  setup: () => {
    const store = useStore();
    const canPlay = computed(() => store.getters["stage/canPlay"]);
    const curtain = computed(() => store.state.stage.curtain);
    const config = computed(() => store.getters["stage/config"]);
    const duration = 3000;

    const curtainEnter = (el, complete) => {
      let anotherCurtain; // Needed for close and open animation
      switch (config.value?.animations?.curtain) {
        case "fade":
          anime({
            targets: el,
            opacity: [0, 1],
            duration,
            complete,
          });
          break;
        case "close":
          anotherCurtain = el.cloneNode(true);
          el.parentElement.appendChild(anotherCurtain);
          el.style.transformOrigin = "0 0";
          anime({
            targets: el,
            scaleX: [0, 0.5],
            duration,
            complete,
          });
          anotherCurtain.style.transformOrigin = "100% 0";
          anime({
            targets: anotherCurtain,
            scaleX: [0, 0.5],
            duration,
          });
          break;
        default:
          anime({
            targets: el,
            scaleY: [0, 1],
            duration,
            complete,
          });
      }
    };
    const curtainLeave = (el, complete) => {
      let anotherCurtain;
      switch (config.value?.animations?.curtain) {
        case "fade":
          anime({
            targets: el,
            opacity: [1, 0],
            duration,
            complete,
          });
          break;
        case "close":
          anotherCurtain = el.parentElement.querySelectorAll(".curtain")[1];
          el.style.transformOrigin = "0 0";
          anime({
            targets: el,
            scaleX: [0.5, 0],
            duration,
            complete,
          });
          if (anotherCurtain) {
            anotherCurtain.style.transformOrigin = "100% 0";
            anime({
              targets: anotherCurtain,
              scaleX: [0.5, 0],
              duration,
              complete: () => anotherCurtain.remove(),
            });
          }
          break;
        default:
          anime({
            targets: el,
            scaleY: 0,
            duration,
            complete,
          });
      }
    };

    return {
      canPlay,
      curtain,
      curtainEnter,
      curtainLeave,
    };
  },
};
</script>

<style>
</style>