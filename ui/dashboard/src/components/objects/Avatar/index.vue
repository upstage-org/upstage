<template>
  <Object :object="object">
    <template #menu="slotProps">
      <MenuContent
        :object="object"
        v-bind="slotProps"
        v-model:active="active"
      />
    </template>
  </Object>
</template>

<script>
import { computed, provide } from "@vue/runtime-core";
import Object from "../Object.vue";
import MenuContent from "./ContextMenu";
import { useStore } from "vuex";

export default {
  props: ["object"],
  components: { Object, MenuContent },
  setup: (props) => {
    const store = useStore();
    const holder = computed(() =>
      store.state.stage.sessions.find((s) => s.avatarId === props.object.id)
    );
    provide("holder", holder);

    return { holder };
  },
};
</script>

<style>
</style>