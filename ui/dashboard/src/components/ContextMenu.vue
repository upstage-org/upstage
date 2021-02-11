<template>
  <div @contextmenu.prevent="openMenu">
    <slot name="trigger" />
  </div>
  <transition :css="false" @enter="contextAppear">
    <div
      class="card"
      v-if="isActive"
      v-click-outside="closeMenu"
      :style="{
        position: 'fixed',
        top: position.y + 'px',
        left: position.x + 'px',
        'z-index': 10000,
        overflow: 'visible',
      }"
    >
      <slot name="context" :closeMenu="closeMenu" />
    </div>
  </transition>
</template>

<script>
import { reactive, ref } from "vue";
export default {
  props: ["active"],
  setup: (props) => {
    const isActive = ref(props.active);
    const position = reactive({ x: 100, y: 100 });

    const openMenu = (e) => {
      position.x = e.clientX;
      position.y = e.clientY;
      isActive.value = true;
    };
    const closeMenu = () => (isActive.value = false);

    const contextAppear = (el) => {
      const { width, height, right, bottom } =
        el?.getBoundingClientRect() ?? {};
      if (right > window.innerWidth) {
        position.x = position.x - width;
      }
      if (bottom > window.innerHeight) {
        position.y = position.y - height;
      }
    };

    return { isActive, openMenu, closeMenu, position, contextAppear };
  },
};
</script>

<style>
</style>