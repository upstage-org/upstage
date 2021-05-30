<template>
  <canvas ref="el" />
</template>

<script>
import { useDrawing } from "./composable";
export default {
  props: ["drawing"],
  setup: (props) => {
    const { el } = useDrawing({ ...props.drawing, w: 64, h: 64 });
    return { el };
  },
};
</script>

<style>
</style>