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
      v-bind="$attrs"
      :checked="modelValue"
      @input="$emit('update:modelValue', $event.target.checked)"
      style="display: none"
    />
    <label class="clickable" :for="id">
      <Loading v-if="loading" height="24px" />
      <template v-else>
        <Icon v-if="modelValue" src="toggle_on.svg" size="36" height="24" />
        <Icon v-else src="toggle_off.svg" size="36" height="24" />
      </template>
      {{ label }}
    </label>
  </div>
</template>

<script>
import { v4 as uuidv4 } from "uuid";
import Icon from "components/Icon.vue";
import Loading from "components/Loading.vue";

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
  components: { Icon, Loading },
  setup: () => {
    const id = uuidv4();
    return { id };
  },
};
</script>

<style scoped>
.on-switch-label {
  pointer-events: none;
  position: absolute;
  color: white;
  z-index: 1;
  top: 2px;
}
img {
  vertical-align: middle;
}
</style>
