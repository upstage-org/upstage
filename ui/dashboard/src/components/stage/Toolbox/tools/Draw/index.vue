<template>
  <canvas
    ref="el"
    v-show="isDrawing"
    class="drawing"
    :width="stageSize.width"
    :height="stageSize.height"
    :style="{
      cursor,
      top: stageSize.top + 'px',
      left: stageSize.left + 'px',
    }"
  >
    Your browser does not support the HTML5 canvas tag.
  </canvas>
  <template v-if="isDrawing">
    <div class="drawing-tool">
      <div class="icon is-large">
        <ColorPicker v-model="color" />
      </div>
      <span class="tag is-light is-block">{{ $t("colour") }}</span>
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
        max="200"
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
      <span class="tag is-light is-block">{{ $t("erase") }}</span>
    </div>
    <div class="drawing-tool" @click="undo">
      <div class="icon is-large">
        <Icon size="36" src="undo.svg" />
      </div>
      <span class="tag is-light is-block">{{ $t("undo") }}</span>
    </div>
    <div class="drawing-tool" @click="clearCanvas(true)">
      <div class="icon is-large">
        <Icon size="36" src="clear.svg" />
      </div>
      <span class="tag is-light is-block">{{ $t("clear") }}</span>
    </div>
    <div class="drawing-tool" @click="save('avatar')">
      <div class="icon is-large">
        <Icon size="24" src="check.svg" />
        &nbsp;
        <Icon size="24" src="avatar.svg" />
      </div>
      <span class="tag is-light is-block">Save as Avatar</span>
    </div>
    <div class="drawing-tool" @click="save('prop')">
      <div class="icon is-large">
        <Icon size="24" src="check.svg" />
        &nbsp;
        <Icon size="24" src="prop.svg" />
      </div>
      <span class="tag is-light is-block">Save as Prop</span>
    </div>
    <div class="drawing-tool" @click="cancel">
      <div class="icon is-large">
        <Icon size="36" src="cancel.svg" />
      </div>
      <span class="tag is-light is-block">{{ $t("cancel") }}</span>
    </div>
  </template>
  <template v-else>
    <div @click="create" class="is-pulled-left">
      <div class="icon is-large">
        <Icon src="new.svg" size="36" />
      </div>
      <span class="tag is-light is-block">New Drawing</span>
    </div>
    <div v-for="drawing in drawings" :key="drawing">
      <ContextMenu>
        <template #trigger>
          <Skeleton :data="drawing" />
        </template>
        <template #context>
          <a
            class="panel-block has-text-danger"
            @click="deleteDrawingPermanently(drawing)"
          >
            <span class="panel-icon">
              <Icon src="remove.svg" />
            </span>
            <span>Delete Permanently</span>
          </a>
        </template>
      </ContextMenu>
    </div>
  </template>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import { useDrawable } from "./composable";
import ColorPicker from "@/components/form/ColorPicker";
import Icon from "@/components/Icon";
import ContextMenu from "@/components/ContextMenu";
import Skeleton from "../../Skeleton";
import { v4 as uuidv4 } from "uuid";

export default {
  components: { Skeleton, ColorPicker, Icon, ContextMenu },
  setup: () => {
    const store = useStore();
    const stageSize = computed(() => store.getters["stage/stageSize"]);
    const drawings = computed(() => store.state.stage.board.drawings);
    const isDrawing = computed(() => {
      return store.state.stage.preferences.isDrawing;
    });
    const {
      el,
      cursor,
      getDrawedArea,
      clearCanvas,
      undo,
      toggleErase,
      color,
      size,
      mode,
      history,
    } = useDrawable();
    const create = () => {
      store.commit("stage/SET_ACTIVE_MOVABLE", null);
      store.commit("stage/UPDATE_IS_DRAWING", true);
      clearCanvas(true);
    };
    const cancel = () => {
      store.commit("stage/UPDATE_IS_DRAWING", false);
    };
    const save = (type) => {
      const area = getDrawedArea();
      if (area) {
        const drawingId = uuidv4();
        const commands = [...history];
        store.dispatch("stage/addDrawing", {
          ...area,
          commands,
          type,
          drawingId,
        });
      }
      cancel();
    };

    const deleteDrawingPermanently = (drawing) => {
      store.commit("stage/POP_DRAWING", drawing.drawingId);
      store.getters["stage/objects"]
        .filter((o) => o.drawingId === drawing.drawingId)
        .forEach((o) => {
          store.dispatch("stage/deleteObject", o);
        });
    };

    return {
      isDrawing,
      drawings,
      color,
      size,
      create,
      save,
      cancel,
      el,
      clearCanvas,
      undo,
      toggleErase,
      mode,
      cursor,
      stageSize,
      deleteDrawingPermanently,
    };
  },
};
</script>

<style lang="scss" scoped>
.drawing {
  position: fixed;
  z-index: 1000;
  background-color: hsla(142, 52%, 96%, 0.8);
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