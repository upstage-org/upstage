<template>
  <Object :object="drawing">
    <template #menu="slotProps">
      <MenuContent
        :object="drawing"
        :closeMenu="slotProps.closeMenu"
        v-model:active="active"
      />
    </template>
    <template #render>
      <canvas ref="el"></canvas>
    </template>
  </Object>
</template>

<script>
import Object from "./Object.vue";
import MenuContent from "./Avatar/ContextMenu"; // Drawing should inherit all of avatar behavior
import { useStore } from "vuex";
import { useDrawing } from "@/components/stage/Toolbox/tools/Draw/composable";

export default {
  props: ["drawing"],
  components: { Object, MenuContent },
  setup: (props) => {
    const store = useStore();

    const { el } = useDrawing(props.drawing);

    return { el, store };
  },
};
</script>

<style>
</style>