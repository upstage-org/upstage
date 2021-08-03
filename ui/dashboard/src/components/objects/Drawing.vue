<template>
  <Object :object="object">
    <template #menu="slotProps">
      <MenuContent
        :object="object"
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
import MenuContent from "./Avatar/ContextMenu";
import { useStore } from "vuex";
import { useDrawing } from "@/components/stage/Toolbox/tools/Draw/composable";
import { computed } from "@vue/runtime-core";

export default {
  props: ["object"],
  components: { Object, MenuContent },
  setup: (props) => {
    const store = useStore();

    const drawing = computed(() => ({ ...props.object }));
    const { el } = useDrawing(drawing);

    return { el, store };
  },
};
</script>

<style>
</style>