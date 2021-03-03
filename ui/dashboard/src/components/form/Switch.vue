<template>
  <div class="field is-inline-block is-relative">
    <span
      class="on-switch-label"
      v-if="!!checkedLabel && modelValue"
      style="left: 10px"
    >
      {{ checkedLabel }}
    </span>
    <span
      class="on-switch-label"
      v-if="!!uncheckedLabel && !modelValue"
      style="left: 25px"
    >
      {{ uncheckedLabel }}
    </span>
    <input
      :id="id"
      type="checkbox"
      :class="`switch ${className}`"
      v-bind="$attrs"
      :checked="modelValue"
      @input="$emit('update:modelValue', $event.target.checked)"
    />
    <label :for="id" :class="{ 'is-loading': loading }">{{ label }}</label>
  </div>
</template>

<script>
import { v4 as uuidv4 } from "uuid";
export default {
  props: [
    "className",
    "modelValue",
    "label",
    "checkedLabel",
    "uncheckedLabel",
    "loading",
  ],
  emits: ["update:modelValue"],
  setup: () => {
    const id = uuidv4();
    return { id };
  },
};
</script>

<style>
.on-switch-label {
  pointer-events: none;
  position: absolute;
  color: white;
  z-index: 1;
  top: 2px;
}
</style>