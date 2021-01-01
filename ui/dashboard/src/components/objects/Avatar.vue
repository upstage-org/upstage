<template>
  <DragResize
    :initW="100"
    :initH="100"
    v-model:x="x"
    v-model:y="y"
    v-model:w="w"
    v-model:h="h"
    v-model:active="active"
    :draggable="true"
    :resizable="true"
    @activated="print('activated')"
    @deactivated="print('deactivated')"
    @drag-start="print('drag-start')"
    @resize-start="print('resize-start')"
    @dragging="print('dragging')"
    @resizing="print('resizing')"
    @drag-end="print('drag-end')"
    @resize-end="print('resize-end')"
  >
    <Image :src="avatar.src" />
  </DragResize>
</template>

<script>
import DragResize from "vue3-draggable-resizable";
import Image from "@/components/Image";

export default {
  props: ["avatar"],
  components: { DragResize, Image },
  methods: {
    print(val) {
      console.log(val);
    },
  },
  setup(props) {
    return {
      x: props.avatar.x,
      y: props.avatar.y,
      h: 100,
      w: 100,
      active: false,
    };
  },
};
</script>

<style>
</style>