<template>
  <div @contextmenu.prevent="openMenu">
    <slot name="trigger" />
  </div>
  <div
    class="card"
    v-if="isActive"
    v-click-outside="closeMenu"
    :style="{
      position: 'fixed',
      top: position.y + 'px',
      left: position.x + 'px',
      'z-index': 100,
    }"
  >
    <slot name="context" />
  </div>
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

    return { isActive, openMenu, closeMenu, position };
  },
};
</script>

<style>
</style>