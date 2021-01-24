<template>
  <template v-if="isDrawing">
    <canvas
      ref="el"
      width="3840"
      height="2160"
      class="drawing"
      :style="{ cursor }"
    >
      Your browser does not support the HTML5 canvas tag.
    </canvas>
    <div class="drawing-tool">
      <div class="icon is-large">
        <input type="color" v-model="color" />
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
        <i class="fas fa-eraser fa-2x"></i>
      </div>
      <span class="tag is-light is-block">Erase</span>
    </div>
    <div class="drawing-tool" @click="undo">
      <div class="icon is-large">
        <i class="fas fa-undo fa-2x"></i>
      </div>
      <span class="tag is-light is-block">Undo</span>
    </div>
    <div class="drawing-tool" @click="clearCanvas">
      <div class="icon is-large">
        <i class="fas fa-broom fa-2x"></i>
      </div>
      <span class="tag is-light is-block">Clear</span>
    </div>
    <div class="drawing-tool" @click="save">
      <div class="icon is-large">
        <i class="fas fa-save fa-2x"></i>
      </div>
      <span class="tag is-light is-block">Save</span>
    </div>
  </template>
  <template v-else>
    <div @click="create">
      <div class="icon is-large">
        <i class="fas fa-plus fa-2x"></i>
      </div>
      <span class="tag is-light is-block">New</span>
    </div>
  </template>
  <div v-for="drawing in drawings" :key="drawing">
    <Skeleton :data="drawing" />
  </div>
</template>

<script>
import { computed, ref } from "vue";
import { useStore } from "vuex";
import { useDrawing } from "./composable";
import Skeleton from "@/components/objects/Skeleton";
export default {
  components: { Skeleton },
  setup: () => {
    const store = useStore();
    const drawings = computed(() => store.state.stage.board.drawings);
    const isDrawing = computed(() => {
      console.log(store.state.stage.board.drawings);
      return store.state.stage.preferences.isDrawing;
    });
    const color = ref();
    const size = ref(10);
    const mode = ref("draw");
    const { el, cursor, cropImageFromCanvas, clearCanvas, undo } = useDrawing(
      color,
      size,
      mode
    );
    const create = () => {
      store.commit("stage/UPDATE_IS_DRAWING", true);
    };
    const save = () => {
      const drawing = cropImageFromCanvas();
      if (drawing) {
        store.dispatch("stage/addDrawing", drawing);
      }
    };
    const toggleErase = () => {
      if (mode.value === "erase") {
        mode.value = "draw";
      } else {
        mode.value = "erase";
      }
    };

    return {
      isDrawing,
      drawings,
      color,
      size,
      create,
      save,
      el,
      clearCanvas,
      undo,
      toggleErase,
      mode,
      cursor,
    };
  },
};
</script>

<style lang="scss" scoped>
@import "@/styles/mixins.scss";

.drawing {
  position: fixed;
  top: 0;
  left: 0vh;
  z-index: 1000;
  background-color: rgba($color: white, $alpha: 0.5);
  backdrop-filter: blur(5px);
}
.drawing-tool {
  background-color: rgba($color: white, $alpha: 0.5);
  z-index: 1001;
  position: relative;
  vertical-align: top;
  &:first-of-type {
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
  }
  &:last-of-type {
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
  }
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
.fas.fa-eraser {
  @include gradientText(#ffffff, #ff6b6b);
}
.fas.fa-undo {
  @include gradientText(#3498db, #2c3e50);
}
.fas.fa-broom {
  @include gradientText(#ffb347, #a83279);
}
.fas.fa-save {
  @include gradientText(#6441a5, #2a0845);
}
.fas.fa-plus {
  @include gradientText(#30ac45, #6fb1fc);
}
</style>