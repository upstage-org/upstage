<template>
  <Object :object="avatar">
    <template #menu="slotProps">
      <MenuContent
        :object="avatar"
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
  props: ["avatar"],
  components: { Object, MenuContent },
};
</script>

<style>
</style>