<template>
  <div class="field" :class="{ 'is-horizontal': horizontal }">
    <label class="label" v-if="label">{{ label }}</label>
    <div
      class="control"
      :class="{
        'has-icons-left': left,
        'has-icons-right': right,
        'is-expanded': expanded,
      }"
    >
      <input
        class="input"
        :class="{ 'is-danger': isTouched && (isRequired || error) }"
        :type="type"
        :placeholder="placeholder"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        @blur="stateTouched = true"
      />
      <slot name="left">
        <span class="icon is-small is-left" v-if="left">
          <i :class="left"></i>
        </span>
      </slot>
      <slot name="right">
        <span class="icon is-small is-right" v-if="right">
          <i :class="right"></i>
        </span>
      </slot>
    </div>
    <p class="help is-danger" v-if="isTouched && error">
      <span>{{ error }}</span>
    </p>
    <p class="help is-danger" v-if="isRequired">
      <span v-if="requiredMessage">{{ requiredMessage }}</span>
      <span v-else>{{ label }} is required</span>
    </p>
    <template v-else>
      <p class="help" v-if="help">{{ help }}</p>
    </template>
  </div>
</template>

<script>
import { computed, ref } from "vue";
export default {
  props: {
    required: {
      type: Boolean,
      default: false,
    },
    requiredMessage: {
      type: String,
    },
    modelValue: {
      type: String,
    },
    label: {
      type: String,
    },
    type: {
      type: String,
      default: "text",
    },
    placeholder: {
      type: String,
    },
    left: {
      type: String,
    },
    right: {
      type: String,
    },
    horizontal: {
      type: Boolean,
      default: false,
    },
    expanded: {
      type: Boolean,
      default: false,
    },
    help: {
      type: String,
    },
    error: {
      type: String,
    },
    touched: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["update:modelValue"],
  setup: (props) => {
    const stateTouched = ref(false);
    const isTouched = computed(() => props.touched || stateTouched.value);
    const isRequired = computed(
      () => props.required && isTouched.value && !props.modelValue
    );

    return { isRequired, stateTouched, isTouched };
  },
};
</script>

<style>
</style>