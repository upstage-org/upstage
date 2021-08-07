<template>
  <canvas
    ref="el"
    class="drawing"
    :width="stageSize.width"
    :height="stageSize.height"
    :style="{
      cursor,
      top: stageSize.top + 'px',
      left: stageSize.left + 'px',
      'pointer-events': none,
    }"
  >
    Your browser does not support the HTML5 canvas tag.
  </canvas>
  <div class="drawing-tool">
    <div class="icon is-large">
      <ColorPicker v-model="color" />
    </div>
    <span class="tag is-light is-block">Color</span>
  </div>
  <div class="drawing-tool" style="width: 200px">
    <div class="size-preview">
      <div
        class="dot"
        :style="{
          width: size + 'px',
          height: size + 'px',
          'background-color': color,
        }"
        @click="mode = 'draw'"
      />
    </div>
    <input
      class="slider is-fullwidth m-0 is-dark"
      step="1"
      min="1"
      max="50"
      type="range"
      v-model="size"
    />
  </div>
  <div
    class="drawing-tool"
    @click="toggleErase"
    :class="{
      active: mode === 'erase',
    }"
  >
    <div class="icon is-large">
      <Icon size="36" src="erase.svg" />
    </div>
    <span class="tag is-light is-block">Erase</span>
  </div>
  <div class="drawing-tool" @click="undo">
    <div class="icon is-large">
      <Icon size="36" src="undo.svg" />
    </div>
    <span class="tag is-light is-block">Undo</span>
  </div>
  <div class="drawing-tool" @click="clear">
    <div class="icon is-large">
      <Icon size="36" src="clear.svg" />
    </div>
    <span class="tag is-light is-block">Clear</span>
  </div>
</template>

<script>
import { computed, onMounted, onUnmounted, watch } from "vue";
import { useStore } from "vuex";
import ColorPicker from "@/components/form/ColorPicker";
import Icon from "@/components/Icon";
import { useDrawable } from "./Draw/composable";

export default {
  components: { ColorPicker, Icon },
  setup: () => {
    const store = useStore();
    const stageSize = computed(() => store.getters["stage/stageSize"]);
    const isDrawing = computed(() => {
      return store.state.stage.preferences.isDrawing;
    });
    const { el, cursor, toggleErase, color, size, mode, history, clearCanvas } =
      useDrawable();

    onMounted(() => {
      store.commit("stage/UPDATE_IS_DRAWING", true);
    });

    onUnmounted(() => {
      store.commit("stage/UPDATE_IS_DRAWING", false);
    });

    watch(history, (val) => {
      if (history.length) {
        let command = val[0];
        const ratio = 1 / stageSize.value.height;
        command = {
          ...command,
          size: command.size * ratio,
          x: command.x * ratio,
          y: command.y * ratio,
          lines: command.lines.map((line) => ({
            x: line.x * ratio,
            y: line.y * ratio,
            fromX: line.fromX * ratio,
            fromY: line.fromY * ratio,
          })),
        };
        store.dispatch("stage/sendDrawWhiteboard", command);
        clearCanvas(true);
      }
    });

    const undo = () => {
      store.dispatch("stage/sendUndoWhiteboard");
      clearCanvas(true);
    };

    const clear = () => {
      store.dispatch("stage/sendClearWhiteboard");
      clearCanvas(true);
    };

    return {
      isDrawing,
      color,
      size,
      el,
      clear,
      undo,
      toggleErase,
      mode,
      cursor,
      stageSize,
    };
  },
};
</script>

<style lang="scss" scoped>
.drawing {
  position: fixed;
  z-index: 1000;
}
.drawing-tool {
  z-index: 1001;
  position: relative;
  vertical-align: top;
}
.size-preview {
  display: flex;
  width: 100%;
  height: 48px;
}
.dot {
  margin: auto;
  background-color: black;
  border-radius: 100%;
}
</style>