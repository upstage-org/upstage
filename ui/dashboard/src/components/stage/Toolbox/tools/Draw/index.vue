<template>
  <template v-if="isDrawing">
    <drawing-canvas :color="color" :size="size" />
    <div class="drawing-tool">
      <input type="color" v-model="color" />
    </div>
    <div class="drawing-tool">
      <div
        v-for="s in sizes"
        :key="s"
        @click="size = s"
        class="dot"
        :class="{ active: size === s }"
        :style="{ width: s * 2 + 'px', height: s * 2 + 'px' }"
      ></div>
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
import DrawingCanvas from "./DrawingCanvas";
export default {
  components: {
    DrawingCanvas,
  },
  setup: () => {
    const store = useStore();
    const isDrawing = computed(() => store.state.stage.preferences.isDrawing);
    const color = ref();
    const size = ref(2);
    const sizes = [2, 4, 6, 8, 10];
    const create = () => {
      store.commit("stage/UPDATE_IS_DRAWING", true);
    };
    const save = () => {
      store.commit("stage/UPDATE_IS_DRAWING", false);
    };
    return { isDrawing, color, size, sizes, create, save };
  },
};
</script>

<style lang="scss" scoped>
.drawing-tool {
  z-index: 1001;
  position: relative;
  vertical-align: top;
}
input[type="color"] {
  cursor: pointer;
  width: 100%;
  height: 100%;
}
.dot {
  float: left;
  margin: 5px;
  background-color: black;
  border-radius: 100%;
  &:hover,
  &.active {
    box-shadow: 0 0 5px #30ac45;
  }
}
</style>