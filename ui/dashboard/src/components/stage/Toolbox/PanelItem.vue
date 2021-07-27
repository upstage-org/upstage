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

<style lang="scss" scoped>
.panel-icon {
  margin: auto;
  img {
    filter: grayscale(100%);
  }
}
.panel-block.is-active,
.panel-block:hover {
  border: none;
  .panel-icon {
    img {
      filter: none;
    }
    transform: scale(1.5);
  }
}
</style>