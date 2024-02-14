<template>
  <div :style="{ opacity: canPlay ? 0.5 : 1 }">
    <transition @enter="curtainEnter" @leave="curtainLeave">
      <img
        v-if="curtain"
        :key="curtain"
        :src="curtain"
        class="curtain"
        :class="{ 'dual-left': dualCurtain }"
      />
    </transition>
    <transition @enter="dualCurtainEnter" @leave="dualCurtainLeave">
      <img
        v-if="dualCurtain && curtain"
        :key="curtain"
        :src="curtain"
        class="curtain"
        :class="{ 'dual-right': dualCurtain }"
      />
    </transition>
  </div>
</template>

<script>
import { computed } from "vue";
import anime from "animejs";
import { useStore } from "vuex";
export default {
  setup: () => {
    const store = useStore();
    const canPlay = computed(() => store.getters["stage/canPlay"]);
    const curtain = computed(() => store.state.stage.curtain);
    const config = computed(() => store.getters["stage/config"]);
    const curtainSpeed = computed(
      () => config.value?.animations?.curtainSpeed ?? 3000,
    );

    const curtainEnter = (el, complete) => {
      const duration = curtainSpeed.value;
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
          el.style.transformOrigin = "0 0";
          anime({
            targets: el,
            scaleX: [0, 1],
            duration,
            complete,
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
      const duration = curtainSpeed.value;
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
          el.style.transformOrigin = "0 0";
          anime({
            targets: el,
            scaleX: [1, 0],
            duration,
            complete,
          });
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

    const dualCurtain = computed(
      () => config.value?.animations?.curtain === "close",
    );

    const dualCurtainEnter = (el, complete) => {
      const duration = curtainSpeed.value;
      el.style.transformOrigin = "100% 0";
      anime({
        targets: el,
        scaleX: [0, 1],
        duration,
        complete,
      });
    };

    const dualCurtainLeave = (el, complete) => {
      const duration = curtainSpeed.value;
      el.style.transformOrigin = "100% 0";
      anime({
        targets: el,
        scaleX: [1, 0],
        duration,
        complete,
      });
    };

    return {
      canPlay,
      curtain,
      curtainEnter,
      curtainLeave,
      dualCurtain,
      dualCurtainEnter,
      dualCurtainLeave,
    };
  },
};
</script>

<style scoped>
.curtain {
  pointer-events: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  transform-origin: top;
}
.dual-left {
  width: 50vw;
}
.dual-right {
  width: 50vw;
  left: 50vw;
}
</style>
