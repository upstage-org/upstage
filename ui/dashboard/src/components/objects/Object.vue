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
          v-if="loggedIn"
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
            :src="src"
            :opacity="(object.opacity ?? 1) * (isDragging ? 0.5 : 1)"
          />
        </DragResize>
        <Image
          :src="src"
          v-if="isDragging || !loggedIn"
          :style="{
            width: position.w + 'px',
            height: position.h + 'px',
            position: 'fixed',
            left: (isDragging ? beforeDragPosition.x : position.x) + 'px',
            top: (isDragging ? beforeDragPosition.y : position.y) + 'px',
          }"
          :opacity="object.opacity"
        />
      </template>
      <template #context="slotProps" v-if="loggedIn">
        <MenuContent
          :object="object"
          :closeMenu="slotProps.closeMenu"
          v-model:active="active"
        />
      </template>
    </ContextMenu>
  </div>
</template>

<script>
import { useStore } from "vuex";
import { computed, reactive, ref, watch } from "vue";
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
    const loggedIn = computed(() => store.getters["auth/loggedIn"]);

    // Local state
    const active = ref(false);
    const position = reactive({ ...props.object, y: 0 });
    const isDragging = ref(false);
    const beforeDragPosition = ref();

    watch(
      props.object,
      () => {
        if (position.src !== props.object.src) {
          if (!props.object.autoplayFrames) {
            anime({
              targets: el.value.getElementsByClassName("the-object"),
              rotate: ["-3deg", "3deg", "0deg"],
              duration: config.animateDuration,
              easing: "easeInOutQuad",
              complete: () => (position.src = props.object.src),
            });
          }
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
      if (loggedIn.value) {
        store.dispatch("stage/deleteObject", props.object);
      }
    };

    const setAsPrimaryAvatar = () => {
      if (loggedIn.value) {
        const { name, id } = props.object;
        store.dispatch("user/setAvatarId", { id, name }).then(props.closeMenu);
      }
    };

    const frameAnimation = reactive({
      interval: null,
      currentFrame: null,
    });
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
    const src = computed(() => {
      if (props.object.autoplayFrames) {
        return frameAnimation.currentFrame;
      } else {
        return props.object.src;
      }
    });

    return {
      el,
      loggedIn,
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
      src,
    };
  },
};
</script>

<style scoped lang="scss">
.object {
  z-index: 10;
}
</style>