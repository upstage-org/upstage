<template>
  <Object :object="object">
    <template #menu="slotProps">
      <MenuContent
        :object="object"
        :closeMenu="slotProps.closeMenu"
        v-model:active="active"
      />
    </template>
  </Object>
</template>

<script>
import Object from "../Object.vue";
import MenuContent from "./ContextMenu";

export default {
  props: ["object"],
  components: { Object, MenuContent },
};
</script>

<style>
</style>