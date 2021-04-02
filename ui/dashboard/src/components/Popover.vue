<template>
  <div @mouseover="mouseover" @mouseout="mouseout" class="popover">
    <slot name="trigger" />

    <transition @enter="enter">
      <div v-if="position" class="card">
        <slot />
      </div>
    </transition>
  </div>
</template>

<script>
import { ref } from "@vue/reactivity";
import anime from "animejs";
export default {
  setup: () => {
    const position = ref();
    const mouseover = (e) => {
      position.value = {
        x: e.clientX,
        y: e.clientY,
      };
    };

    const mouseout = () => {
      position.value = null;
    };

    const enter = (el, complete) => {
      anime({
        targets: el,
        complete,
      });
    };

    return { mouseover, mouseout, position, enter };
  },
};
</script>

<style scoped>
.popover {
  display: inline;
  cursor: pointer;
}
</style>