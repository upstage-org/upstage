<template>
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
    @drag-end="dragEnd"
    @resize-end="resizeEnd"
  >
    <Image :src="object.src" />
  </DragResize>
</template>

<script>
import DragResize from "vue3-draggable-resizable";
import Image from "@/components/Image";
import { useStore } from "vuex";
import { computed } from "vue";

export default {
  props: ["object"],
  components: { DragResize, Image },
  setup(props) {
    const store = useStore();
    const position = computed(() => props.object);

    const dragEnd = (e) => {
      store.dispatch("stage/shapeObject", {
        ...props.object,
        ...e,
      });
    };

    const resizeEnd = (e) => {
      store.dispatch("stage/shapeObject", {
        ...props.object,
        ...e,
      });
    };

    return {
      print,
      dragEnd,
      resizeEnd,
      active: false,
      position,
    };
  },
};
</script>

<style scoped>
.object {
  z-index: 10;
}
</style>