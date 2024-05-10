<template>
  <input
    type="color"
    :value="modelValue"
    @input="$emit('update:modelValue', $event.target.value)"
  />
</template>

<script>
export default {
  props: ["modelValue"],
  emits: ["update:modelValue"],
};
</script>

<style>
input[type="color"] {
  cursor: pointer;
  width: 48px;
  height: 48px;
  flex: none;
}
</style>
