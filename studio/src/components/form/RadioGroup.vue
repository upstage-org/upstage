<template>
  <HorizontalField v-bind="$attrs">
    <Switch class="is-rounded is-success mr-2" v-for="item in data" :key="item"
      :model-value="renderValue(item) === modelValue"
      @update:model-value="$emit('update:modelValue', renderValue(item))" :label="renderLabel(item)" />
    <a-tooltip :title="clearTooltip">
      <button v-if="allowClear && modelValue" @click="$emit('update:modelValue', null)"
        class="button is-danger ml-2 is-small">
        <span class="icon">
          <i class="fas fa-times"></i>
        </span>
        <span>{{ $t("clear") }}</span>
      </button>
    </a-tooltip>
  </HorizontalField>
</template>

<script>
import HorizontalField from "./HorizontalField";
import Switch from "./Switch";

export default {
  props: {
    data: Array,
    modelValue: String,
    renderLabel: {
      type: Function,
      default: (item) => item,
    },
    renderValue: {
      type: Function,
      default: (item) => item,
    },
    allowClear: {
      type: Boolean,
      default: false,
    },
    clearTooltip: String,
  },
  emits: ["update:modelValue"],
  components: { HorizontalField, Switch },
  setup: (props) => {
    console.log(props);
    return {};
  },
};
</script>

<style></style>
