<template>
  <div
    ref="el"
    :style="{
      position: 'absolute',
    }"
    @mousedown="showControls(true, $event)"
    v-click-outside="(e) => showControls(false, e)"
  >
    <slot />
  </div>
  <div
    v-if="isDragging"
    :style="{
      position: 'absolute',
      left: object.x + 'px',
      top: object.y + 'px',
      width: object.w + 'px',
      height: object.h + 'px',
    }"
  >
    <slot />
  </div>
</template>

<script>
/* eslint-disable vue/no-mutating-props */

import { ref } from "@vue/reactivity";
import { onMounted, onUnmounted, watch, watchEffect } from "@vue/runtime-core";
import Moveable from "moveable";
import { useStore } from "vuex";
import anime from "animejs";

export default {
  props: ["object", "controlable", "active"],
  emits: ["update:active"],
  setup: (props, { emit }) => {
    const el = ref();
    const isDragging = ref(false);

    const store = useStore();
    const config = store.getters["stage/config"];
    let moveable;

    onMounted(() => {
      moveable = new Moveable(document.body, {
        draggable: true,
        resizable: true,
        rotatable: true,
        origin: false,
      });

      moveable
        .on("dragStart", () => {
          isDragging.value = true;
        })
        .on("drag", ({ target, left, top }) => {
          target.style.left = `${left}px`;
          target.style.top = `${top}px`;
        })
        .on("dragEnd", ({ lastEvent, target }) => {
          if (lastEvent) {
            target.style.left = `${props.object.x}px`;
            target.style.top = `${props.object.y}px`;
            store.dispatch("stage/shapeObject", {
              ...props.object,
              x: lastEvent.left,
              y: lastEvent.top,
            });
          }
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

    const showControls = (iShowing, e) => {
      if (moveable) {
        if (props.controlable && iShowing) {
          moveable.setState(
            {
              target: el.value,
            },
            () => {
              moveable.dragStart(e);
            }
          );
          emit("update:active", true);
        } else {
          if (!e || e.target.id === "board") {
            moveable.setState(
              {
                target: null,
              },
              () => {
                emit("update:active", false);
              }
            );
          }
        }
      }
    };

    let animation;
    watch(
      props.object,
      () => {
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
        console.log(left, top, width, height, animation);
        animation?.pause(true);
        showControls(false);
        emit("update:active", false);
        animation = anime({
          targets: el.value,
          left,
          top,
          width,
          height,
          rotate,
          ...(moveSpeed > 1000 ? { easing: "easeInOutQuad" } : {}),
          duration: moveSpeed ?? config.animateDuration,
        });
      },
      { deep: true }
    );

    onMounted(() => {
      const { x, y, w, h } = props.object;
      el.value.style.width = `${w}px`;
      el.value.style.height = `${h}px`;
      el.value.style.left = `${x}px`;
      el.value.style.top = `${y}px`;
    });
    watchEffect(() => {
      if (!props.controlable) {
        showControls(false);
      }
    });
    onUnmounted(() => {
      moveable.destroy();
    });

    return { el, showControls, isDragging };
  },
};
</script>

<style>
</style>