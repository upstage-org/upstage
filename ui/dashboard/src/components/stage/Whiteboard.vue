<template>
  <canvas class="whiteboard" ref="el" :style="{ top: stageSize.top + 'px' }" />
</template>

<script>
import { computed, toRaw, watch } from "@vue/runtime-core";
import { useDrawing } from "./Toolbox/tools/Draw/composable";
import { useStore } from "vuex";
export default {
  setup: () => {
    const store = useStore();
    const stageSize = computed(() => store.getters["stage/stageSize"]);
    const whiteboard = computed(() => store.state.stage.board.whiteboard);
    const drawing = computed(() => ({
      w: stageSize.value.width,
      h: stageSize.value.height,
      commands: toRaw(whiteboard.value),
      original: {
        x: 0,
        y: 0,
        w: stageSize.value.width,
        h: stageSize.value.height,
      },
    }));
    watch(drawing, console.log);
    const { el } = useDrawing(drawing);
    return { el, stageSize };
  },
};
</script>

<style scoped>
.whiteboard {
  position: fixed;
  pointer-events: none;
}
</style>