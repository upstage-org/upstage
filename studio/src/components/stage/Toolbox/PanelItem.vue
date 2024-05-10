<template>
  <a-tooltip placement="rightBottom">
    <template #title>{{ label ?? name }}</template>
    <a @click="
      changeTool(name);
    $emit('click');
    " :class="{ 'is-active': tool?.value === name }" class="panel-block button">
      <span class="panel-icon">
        <Icon :src="icon" />
      </span>
    </a>
  </a-tooltip>
</template>

<script>
import Icon from "components/Icon.vue";
export default {
  props: ["name", "label", "icon"],
  inject: ["tool", "changeTool"],
  emits: ["click"],
  components: { Icon },
};
</script>

<style lang="scss" scoped></style>
