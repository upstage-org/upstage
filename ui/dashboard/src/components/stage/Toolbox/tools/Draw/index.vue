<template>
  <template v-if="isDrawing">
    <canvas ref="el" width="3840" height="2160" class="drawing">
      Your browser does not support the HTML5 canvas tag.
    </canvas>
    <div class="drawing-tool">
      <input type="color" v-model="color" />
    </div>
    <div class="drawing-tool">
      <div class="size-preview">
        <div
          class="dot"
          :style="{
            width: size + 'px',
            height: size + 'px',
            'background-color': color,
          }"
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
    <div class="drawing-tool" @click="undo">
      <div class="icon is-large">
        <i class="fas fa-undo fa-2x"></i>
      </div>
      <div>Undo</div>
    </div>
    <div class="drawing-tool" @click="clearCanvas">
      <div class="icon is-large">
        <i class="fas fa-broom fa-2x"></i>
      </div>
      <div>Clear</div>
    </div>
    <div class="drawing-tool" @click="save">
      <div class="icon is-large">
        <i class="fas fa-save fa-2x"></i>
      </div>
      <div>Save</div>
    </div>
  </template>
  <template v-else>
    <div @click="create">
      <div class="icon is-large">
        <i class="fas fa-plus fa-2x"></i>
      </div>
      <div>New</div>
    </div>
  </template>
</template>

<script>
import { computed, ref } from "vue";
import { useStore } from "vuex";
import { useDrawing } from "./composable";
export default {
  setup: () => {
    const store = useStore();
    const isDrawing = computed(() => store.state.stage.preferences.isDrawing);
    const color = ref();
    const size = ref(10);
    const { el, cropImageFromCanvas, clearCanvas, undo } = useDrawing(
      color,
      size
    );
    const create = () => {
      store.commit("stage/UPDATE_IS_DRAWING", true);
    };
    const save = () => {
      const drawing = cropImageFromCanvas();
      store.dispatch("stage/addDrawing", drawing);
    };
    return { isDrawing, color, size, create, save, el, clearCanvas, undo };
  },
};
</script>

<style lang="scss" scoped>
.drawing-tool {
  z-index: 1001;
  position: relative;
  vertical-align: top;
}
.drawing {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
  background-color: rgba($color: #30ac45, $alpha: 0.3);
}
input[type="color"] {
  cursor: pointer;
  width: 100%;
  height: 100%;
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