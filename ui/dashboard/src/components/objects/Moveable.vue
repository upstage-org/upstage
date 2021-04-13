<template>
  <div
    ref="el"
    :style="{
      position: 'absolute',
    }"
    @mousedown="showControls($event)"
    v-click-outside="() => showControls(false)"
  >
    <slot />
  </div>
</template>

<script>
/* eslint-disable vue/no-mutating-props */

import { ref } from "@vue/reactivity";
import { onMounted, watchEffect } from "@vue/runtime-core";
import Moveable from "moveable";
import { useStore } from "vuex";
import anime from "animejs";

export default {
  props: ["object", "controlable"],
  setup: (props) => {
    const el = ref();
    const isDragging = ref(false);
    const animation = ref();

    const store = useStore();
    const config = store.getters["stage/config"];
    let moveable;

    onMounted(() => {
      moveable = new Moveable(document.body, {
        draggable: true,
        resizable: true,
        rotatable: true,
      });

      moveable
        .on("dragStart", () => {
          isDragging.value = true;
        })
        .on("drag", ({ target, left, top }) => {
          props.object.x = left;
          props.object.y = top;
          target.style.left = `${left}px`;
          target.style.top = `${top}px`;
        })
        .on("dragEnd", () => {
          store.dispatch("stage/shapeObject", {
            ...props.object,
          });
          isDragging.value = false;
        });

      /* resizable */
      moveable
        .on("resizeStart", () => {
          isDragging.value = true;
        })
        .on("resize", ({ target, width, height, drag: { left, top } }) => {
          props.object.w = width;
          props.object.h = height;
          props.object.x = left;
          props.object.y = top;
          target.style.width = `${width}px`;
          target.style.height = `${height}px`;
          target.style.left = `${left}px`;
          target.style.top = `${top}px`;
        })
        .on("resizeEnd", () => {
          store.dispatch("stage/shapeObject", {
            ...props.object,
          });
          isDragging.value = false;
        });

      moveable
        .on("rotateStart", (e) => {
          e.set(props.object.rotate);
          isDragging.value = true;
        })
        .on("rotate", ({ target, rotate }) => {
          props.object.rotate = rotate;
          target.style.transform = `rotate(${rotate}deg)`;
        })
        .on("rotateEnd", () => {
          store.dispatch("stage/shapeObject", {
            ...props.object,
          });
          isDragging.value = false;
        });
    });

    watchEffect(() => {
      const {
        x: left,
        y: top,
        w: width,
        h: height,
        rotate,
        moveSpeed,
        type,
        isPlaying,
      } = props.object;
      if (isDragging.value || (type === "stream" && isPlaying)) {
        return;
      }
      animation.value?.pause(true);
      animation.value = anime({
        targets: el.value,
        left,
        top,
        width,
        height,
        rotate,
        ...(moveSpeed > 1000 ? { easing: "easeInOutQuad" } : {}),
        duration: moveSpeed ?? config.animateDuration,
      });
    });

    onMounted(() => {
      const { x, y, w, h } = props.object;
      el.value.style.width = `${w}px`;
      el.value.style.height = `${h}px`;
      el.value.style.left = `${x}px`;
      el.value.style.top = `${y}px`;
    });

    const showControls = (e) => {
      console.log(props.controlable);
      if (moveable) {
        if (props.controlable && !!e) {
          moveable.setState(
            {
              target: el.value,
            },
            () => {
              moveable.dragStart(e);
            }
          );
        } else {
          moveable.setState({
            target: null,
          });
        }
      }
    };
    watchEffect(() => {
      if (!props.controlable) {
        showControls(false);
      }
    });

    return { el, showControls };
  },
};
</script>

<style>
</style>