<template>
  <template v-if="isDrawing">
    <drawing-canvas />
    <div class="drawing-tool">
      <div class="icon is-large">
        <i class="fas fa-plus fa-2x"></i>
      </div>
      <div>Brush</div>
    </div>
    <div class="drawing-tool">
      <div class="icon is-large">
        <i class="fas fa-save fa-2x"></i>
      </div>
      <div>Save</div>
    </div>
  </template>
  <template v-else>
    <div>
      <div class="icon is-large">
        <i class="fas fa-plus fa-2x"></i>
      </div>
      <div>New</div>
    </div>
  </template>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import DrawingCanvas from "./DrawingCanvas";
export default {
  components: {
    DrawingCanvas,
  },
  setup: () => {
    const store = useStore();
    const isDrawing = computed(() => store.state.stage.preferences.isDrawing);
    return { isDrawing };
  },
};
</script>

<style lang="scss" scoped>
.drawing-tool {
  z-index: 1001;
  position: relative;
}
</style>