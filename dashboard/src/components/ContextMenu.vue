<template>
  <div @contextmenu.prevent="openMenu" :style="style">
    <slot name="trigger" />
  </div>
  <teleport to="body">
    <transition :css="false" @enter="contextAppear">
      <div
        class="card"
        v-if="$slots.context && isActive"
        v-click-outside="closeMenu"
        :style="{
          position: 'fixed',
          top: position.y + 'px',
          left: position.x + 'px',
          'z-index': 10000,
          overflow: 'visible',
          opacity,
        }"
      >
        <slot name="context" :closeMenu="closeMenu" />
      </div>
    </transition>
  </teleport>
</template>

<script>
import { reactive, ref } from "vue";
export default {
  props: {
    active: Boolean,
    padLeft: {
      type: Number,
      default: 0,
    },
    padTop: {
      type: Number,
      default: 0,
    },
    padRight: {
      type: Number,
      default: 0,
    },
    padBottom: {
      type: Number,
      default: 0,
    },
    opacity: {
      type: Number,
      default: 1,
    },
    style: Object,
    preventClicking: {
      type: Boolean,
      default: false,
    },
  },
  setup: (props) => {
    const isActive = ref(props.active);
    const position = reactive({ x: 100, y: 100 });

    const openMenu = (e) => {
      if (!props.preventClicking) {
        e.currentTarget.click();
      }
      position.x = e.clientX + props.padLeft;
      position.y = e.clientY + props.padTop;
      isActive.value = true;
    };
    const closeMenu = () => (isActive.value = false);

    const contextAppear = (el) => {
      const { width, height, right, bottom } =
        el?.getBoundingClientRect() ?? {};
      if (right > window.innerWidth - props.padRight) {
        position.x = position.x - width;
      }
      if (bottom > window.innerHeight - props.padBottom) {
        position.y = position.y - height;
      }
    };

    return { isActive, openMenu, closeMenu, position, contextAppear };
  },
};
</script>

<style></style>
