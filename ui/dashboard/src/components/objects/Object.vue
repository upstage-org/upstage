<template>
  <OpacitySlider
    :position="position"
    v-model:active="active"
    :object="object"
  />
  <ContextMenu>
    <template #trigger>
      <DragResize
        class="object"
        :initW="100"
        :initH="100"
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
        <Image
          ref="el"
          :src="object.src"
          :opacity="(object.opacity ?? 1) * (isDragging ? 0.5 : 1)"
        />
      </DragResize>
      <Image
        :src="object.src"
        v-if="isDragging"
        :style="{
          width: position.w + 'px',
          height: position.h + 'px',
          position: 'fixed',
          left: beforeDragPosition.x + 'px',
          top: beforeDragPosition.y + 'px',
        }"
        :opacity="object.opacity"
      />
    </template>
    <template #context>
      <div class="card-content">
        <div class="columns">
          <div class="column">First column</div>
          <div class="column">Second column</div>
          <div class="column">Third column</div>
          <div class="column">Fourth column</div>
        </div>
      </div>
    </template>
  </ContextMenu>
</template>

<script>
import DragResize from "vue3-draggable-resizable";
import Image from "@/components/Image";
import ContextMenu from "@/components/ContextMenu";
import OpacitySlider from "./OpacitySlider";
import { useStore } from "vuex";
import { reactive, ref, watch } from "vue";
import anime from "animejs";

export default {
  props: ["object"],
  components: { DragResize, Image, ContextMenu, OpacitySlider },
  setup(props) {
    const store = useStore();
    const active = ref(false);
    const position = reactive({ ...props.object, y: 0 });
    const isDragging = ref(false);
    const beforeDragPosition = ref();
    const el = ref();
    const config = store.getters["stage/config"];

    watch(
      props.object,
      () => {
        anime({
          targets: position,
          ...props.object,
          duration: config.animateDuration,
        });
      },
      { immediate: true }
    );

    const dragStart = () => {
      isDragging.value = true;
      beforeDragPosition.value = {
        x: position.x,
        y: position.y,
      };
    };

    const dragEnd = (e) => {
      store.dispatch("stage/shapeObject", {
        ...props.object,
        ...e,
      });
      position.x = beforeDragPosition.value.x;
      position.y = beforeDragPosition.value.y;
      isDragging.value = false;
    };

    const resizeEnd = (e) => {
      store.dispatch("stage/shapeObject", {
        ...props.object,
        ...e,
      });
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
    };
  },
};
</script>

<style scoped>
.object {
  z-index: 10;
}
</style>