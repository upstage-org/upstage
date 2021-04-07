<template>
  <div
    ref="el"
    tabindex="0"
    @keyup.delete="deleteObject"
    @dblclick="hold"
    :style="{
      ...(object.speak ? { position: 'absolute', 'z-index': 20 } : {}),
    }"
  >
    <OpacitySlider
      :position="position"
      v-model:active="active"
      :object="object"
    />
    <Topping :position="position" :object="object" />
    <ContextMenu
      :pad-left="-stageSize.left"
      :pad-top="-stageSize.top"
      :pad-right="250"
    >
      <template #trigger>
        <DragResize
          v-if="controlable"
          class="object"
          :initW="position.w"
          :initH="position.h"
          v-model:x="position.x"
          v-model:y="position.y"
          v-model:w="position.w"
          v-model:h="position.h"
          v-model:active="active"
          :draggable="true"
          :resizable="true"
          @drag-start="dragStart"
          @drag-end="dragEnd"
          @resize-end="resizeEnd"
        >
          <div
            :style="{
              width: '100%',
              height: '100%',
              opacity: (object.opacity ?? 1) * (isDragging ? 0.5 : 1),
              transform: `rotate(${object.rotate ?? 0}deg)`,
              cursor: 'grab',
            }"
          >
            <slot name="render">
              <Image class="the-object" :src="src" />
            </slot>
          </div>
        </DragResize>
        <template v-if="isDragging || !controlable">
          <div
            :style="{
              position: 'fixed',
              left: (isDragging ? beforeDragPosition.x : position.x) + 'px',
              top: (isDragging ? beforeDragPosition.y : position.y) + 'px',
              width: position.w + 'px',
              height: position.h + 'px',
              opacity: object.opacity,
              transform: `rotate(${object.rotate ?? 0}deg)`,
              cursor: holder ? 'not-allowed' : 'pointer',
            }"
            @mousedown.prevent
          >
            <slot name="render">
              <Image :src="src" />
            </slot>
          </div>
        </template>
      </template>
      <template #context="slotProps" v-if="controlable">
        <slot name="menu" v-bind="slotProps" />
      </template>
    </ContextMenu>
  </div>
</template>

<script>
import { useStore } from "vuex";
import { computed, inject, reactive, ref, watch } from "vue";
import anime from "animejs";
import DragResize from "vue3-draggable-resizable";
import Image from "@/components/Image";
import ContextMenu from "@/components/ContextMenu";
import OpacitySlider from "./OpacitySlider";
import Topping from "./Topping.vue";

export default {
  props: ["object"],
  emits: ["dblclick"],
  components: {
    DragResize,
    Image,
    ContextMenu,
    OpacitySlider,
    Topping,
  },
  setup(props) {
    // Dom refs
    const el = ref();

    // Vuex store
    const store = useStore();
    const config = store.getters["stage/config"];
    const stageSize = computed(() => store.getters["stage/stageSize"]);

    // Local state
    const active = ref(false);
    const position = reactive({ ...props.object });
    const isDragging = ref(false);
    const beforeDragPosition = ref();
    const animation = ref();
    const holder = inject("holder") ?? ref();
    const isHolding = computed(
      () => holder.value?.id === store.state.stage.session
    );
    const holdable = computed(() =>
      ["avatar", "drawing"].includes(props.object.type)
    );
    const controlable = computed(() => {
      return holdable.value ? isHolding.value : store.getters["auth/loggedIn"];
    });

    watch(
      props.object,
      () => {
        const { x, y, h, w, moveSpeed, type, isPlaying } = props.object;
        if (type === "stream" && isPlaying && isDragging.value) {
          return;
        }
        animation.value?.pause(true);
        animation.value = anime({
          targets: position,
          x,
          y,
          h,
          w,
          ...(moveSpeed > 1000 ? { easing: "easeInOutQuad" } : {}),
          duration: moveSpeed ?? config.animateDuration,
        });
      },
      { immediate: true }
    );

    const dragStart = () => {
      animation.value?.pause(true);
      isDragging.value = true;
      beforeDragPosition.value = {
        x: position.x,
        y: position.y,
      };
    };

    const dragEnd = (e) => {
      if (
        e.x !== beforeDragPosition.value.x &&
        e.y !== beforeDragPosition.value.y
      ) {
        store.dispatch("stage/shapeObject", {
          ...props.object,
          ...e,
        });
        position.x = beforeDragPosition.value.x;
        position.y = beforeDragPosition.value.y;
      }
      isDragging.value = false;
    };

    const resizeEnd = (e) => {
      store.dispatch("stage/shapeObject", {
        ...props.object,
        ...e,
      });
    };

    const deleteObject = () => {
      if (controlable.value) {
        store.dispatch("stage/deleteObject", props.object);
      }
    };

    const frameAnimation = reactive({
      interval: null,
      currentFrame: null,
    });
    if (props.object.multi) {
      watch(
        () => props.object.autoplayFrames,
        () => {
          const { autoplayFrames, frames, src } = props.object;
          clearInterval(frameAnimation.interval);
          if (autoplayFrames) {
            frameAnimation.currentFrame = src;
            frameAnimation.interval = setInterval(() => {
              let nextFrame = frames.indexOf(frameAnimation.currentFrame) + 1;
              if (nextFrame >= frames.length) {
                nextFrame = 0;
              }
              frameAnimation.currentFrame = frames[nextFrame];
            }, autoplayFrames);
          }
        },
        {
          immediate: true,
        }
      );
    }
    const src = computed(() => {
      if (props.object.autoplayFrames && props.object.multi) {
        return frameAnimation.currentFrame;
      } else {
        return props.object.src;
      }
    });

    const hold = () => {
      if (holdable.value && !holder.value) {
        store.dispatch("user/setAvatarId", props.object.id);
      }
    };

    return {
      el,
      print,
      dragStart,
      dragEnd,
      resizeEnd,
      active,
      position,
      beforeDragPosition,
      isDragging,
      deleteObject,
      src,
      stageSize,
      hold,
      holder,
      isHolding,
      holdable,
      controlable,
    };
  },
};
</script>

<style lang="scss">
@import "@/styles/bulma";
@import "@/styles/mixins";

div[tabindex] {
  outline: none;
}
.object {
  z-index: 10;
}
</style>