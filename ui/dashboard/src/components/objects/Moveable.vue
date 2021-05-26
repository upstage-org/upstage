<template>
  <div
    ref="el"
    :style="{
      position: 'absolute',
      opacity: isDragging ? 0.5 : 1,
    }"
    @mousedown="clickInside"
    v-click-outside="clickOutside"
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
      transform: `rotate(${object.rotate}deg)`,
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
import { throttle } from "@/utils/common";
import { DURATIONS } from "@/utils/constants";

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
        keepRatio: true,
      });

      const sendMovement = throttle((target, { left, top }) => {
        target.style.left = `${props.object.x}px`;
        target.style.top = `${props.object.y}px`;
        store.dispatch("stage/shapeObject", {
          ...props.object,
          x: left,
          y: top,
        });
      }, DURATIONS.LIVE_ACTION_THROTTLE);
      moveable
        .on("dragStart", () => {
          isDragging.value = true;
        })
        .on("drag", ({ target, left, top }) => {
          emit("update:active", false);
          target.style.left = `${left}px`;
          target.style.top = `${top}px`;
          if (props.object.liveAction) {
            sendMovement(target, { left, top });
          }
        })
        .on("dragEnd", ({ lastEvent, target }) => {
          if (lastEvent) {
            sendMovement(target, lastEvent);
          }
          isDragging.value = false;
        });

      const sendResize = throttle((target, { width, height, left, top }) => {
        store.dispatch("stage/shapeObject", {
          ...props.object,
          x: left,
          y: top,
          w: width,
          h: height,
        });
      }, DURATIONS.LIVE_ACTION_THROTTLE);
      moveable
        .on("resizeStart", () => {
          isDragging.value = true;
        })
        .on("resize", ({ target, width, height, drag: { left, top } }) => {
          emit("update:active", false);
          target.style.width = `${width}px`;
          target.style.height = `${height}px`;
          target.style.left = `${left}px`;
          target.style.top = `${top}px`;
          if (props.object.liveAction) {
            sendResize(target, { left, top, width, height });
          }
        })
        .on(
          "resizeEnd",
          ({
            target,
            lastEvent: {
              width,
              height,
              drag: { left, top },
            },
          }) => {
            sendResize(target, { left, top, width, height });
            isDragging.value = false;
            emit("update:active", true);
          }
        );

      const sendRotation = throttle((target, rotate) => {
        target.style.transform = `rotate(${props.object.rotate}deg)`;
        store.dispatch("stage/shapeObject", {
          ...props.object,
          rotate,
        });
      }, DURATIONS.LIVE_ACTION_THROTTLE);
      moveable
        .on("rotateStart", (e) => {
          e.set(props.object.rotate ?? 0);
          isDragging.value = true;
        })
        .on("rotate", ({ target, rotate }) => {
          emit("update:active", false);
          target.style.transform = `rotate(${rotate}deg)`;
          if (props.object.liveAction) {
            sendRotation(target, rotate);
          }
        })
        .on("rotateEnd", ({ target, lastEvent: { rotate } }) => {
          sendRotation(target, rotate);
          isDragging.value = false;
          emit("update:active", true);
        });
    });

    const showControls = (isShowing, e) => {
      if (moveable) {
        if (props.controlable && isShowing) {
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
    };

    const clickInside = (e) => {
      showControls(true, e);
    };

    const clickOutside = (e) => {
      if (!e || e.target.id === "board") {
        showControls(false);
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
        animation?.pause(true);
        moveable?.setState({ target: null });
        animation = anime({
          targets: el.value,
          left,
          top,
          width,
          height,
          rotate,
          ...(moveSpeed > 1000 ? { easing: "linear" } : {}),
          duration: moveSpeed ?? config.animateDuration,
        });
      },
      { deep: true }
    );

    onMounted(() => {
      const { x, y, w, h, rotate } = props.object;
      el.value.style.width = `${w}px`;
      el.value.style.height = `${h}px`;
      el.value.style.left = `${x}px`;
      el.value.style.top = `${y}px`;
      el.value.style.transform = `rotate(${rotate}deg)`;
    });
    watchEffect(() => {
      if (!props.controlable) {
        showControls(false);
      }
    });
    onUnmounted(() => {
      moveable.destroy();
    });

    return { el, showControls, isDragging, clickInside, clickOutside };
  },
};
</script>

<style>
</style>