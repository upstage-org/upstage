<template>
  <Object :object="text">
    <template #menu="slotProps">
      <MenuContent
        :object="text"
        :closeMenu="slotProps.closeMenu"
        v-model:active="active"
      />
    </template>
    <template #render>
      <p
        :style="text"
        class="has-text-centered"
        contenteditable="true"
        v-html="text.content"
      ></p>
    </template>
  </Object>
</template>

<script>
import Object from "./Object.vue";
import MenuContent from "./Avatar/ContextMenu"; // Text should inherit all of avatar behavior

export default {
  props: ["text"],
  components: { Object, MenuContent },
  setup: (props) => {
    console.log(props);
  },
};
</script>

<style>
</style>