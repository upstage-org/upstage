<template>
  <a
    @click="
      changeTool(name);
      $emit('click');
    "
    :class="{ 'is-active': tool.value === name }"
    class="panel-block button has-tooltip-right"
    :data-tooltip="label ?? name"
  >
    <span class="panel-icon">
      <Icon :src="icon" />
    </span>
  </a>
</template>

<script>
import Icon from "@/components/Icon";
export default {
  props: ["name", "label", "icon"],
  inject: ["tool", "changeTool"],
  emits: ["click"],
  components: { Icon },
};
</script>

<style>
.panel-block {
  padding: 0 !important;
}
.panel-icon {
  margin: auto;
}
</style>