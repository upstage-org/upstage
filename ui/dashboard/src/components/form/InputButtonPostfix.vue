<template>
  <div class="control has-icons-right is-fullwidth">
    <input
      ref="el"
      class="input is-rounded"
      :value="modelValue"
      @input="$emit('update:modelValue')"
      @keyup.enter="(e) => $emit('ok', e.target.value)"
      v-bind="$attrs"
    />
    <button
      class="icon is-right clickable button is-primary is-rounded"
      :class="{ 'is-loading': loading }"
      :disabled="loading"
      @click="$emit('ok', el.value)"
    >
      <i :class="icon"></i>
    </button>
  </div>
</template>

<script>
import { ref } from "vue";
export default {
  props: ["icon", "loading", "modelValue"],
  emits: ["update:modelValue", "ok"],
  setup: () => {
    const el = ref();
    return { el };
  },
};
</script>

<style>
</style>