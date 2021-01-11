<template>
  <div
    ref="el"
    tabindex="0"
    @keyup.delete="deleteObject"
    @dblclick="setAsPrimaryAvatar"
  >
    <OpacitySlider
      :position="position"
      v-model:active="active"
      :object="object"
    />
    <Topping :position="position" :object="object" />
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
            class="the-object"
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
      <template #context="slotProps">
        <MenuContent :object="object" :closeMenu="slotProps.closeMenu" />
      </template>
    </ContextMenu>
  </div>
</template>

<script>
import { useStore } from "vuex";
import { reactive, ref, watch } from "vue";
import anime from "animejs";
import DragResize from "vue3-draggable-resizable";
import Image from "@/components/Image";
import ContextMenu from "@/components/ContextMenu";
import MenuContent from "./ContextMenu";
import OpacitySlider from "./OpacitySlider";
import Topping from "./Topping.vue";

export default {
  props: ["object"],
  components: {
    DragResize,
    Image,
    ContextMenu,
    MenuContent,
    OpacitySlider,
    Topping,
  },
  setup(props) {
    // Dom refs
    const el = ref();

    // Vuex store
    const store = useStore();
    const config = store.getters["stage/config"];

    // Local state
    const active = ref(false);
    const position = reactive({ ...props.object, y: 0 });
    const isDragging = ref(false);
    const beforeDragPosition = ref();

    watch(
      props.object,
      () => {
        if (position.src !== props.object.src) {
          anime({
            targets: el.value.getElementsByClassName("the-object"),
            rotate: ["-3deg", "3deg", "0deg"],
            duration: config.animateDuration,
            easing: "easeInOutQuad",
            complete: () => (position.src = props.object.src),
          });
        } else {
          const { x, y, h, w } = props.object;
          anime({
            targets: position,
            x,
            y,
            h,
            w,
            duration: config.animateDuration,
          });
        }
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

    const deleteObject = () => {
      store.dispatch("stage/deleteObject", props.object);
    };

    const setAsPrimaryAvatar = () => {
      const { name, id } = props.object;
      store.dispatch("user/setAvatarId", { id, name }).then(props.closeMenu);
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
      setAsPrimaryAvatar,
    };
  },
};
</script>

<style scoped lang="scss">
.object {
  z-index: 10;
}
</style>