<template>
  <canvas ref="el" />
</template>

<script>
import { computed } from "@vue/runtime-core";
import { useDrawing } from "./composable";
export default {
  props: ["drawing"],
  setup: (props) => {
    const drawing = computed(() => ({ ...props.drawing, w: 64, h: 64 }));
    const { el } = useDrawing(drawing);
    return { el };
  },
};
</script>

<style></style>
