<template>
  <textarea
    ref="el"
    rows="1"
    v-bind="$attrs"
    class="textarea"
    :value="modelValue"
    @input="handleInput"
    @keydown.enter="submit"
  ></textarea>
</template>

<script>
import { onMounted, ref, watch } from "@vue/runtime-core";
export default {
  props: ["modelValue"],
  emits: ["update:modelValue", "ref", "submit"],
  setup: (props, { emit }) => {
    const el = ref();
    onMounted(() => {
      emit("ref", el.value);
    });
    const handleInput = (e) => {
      emit("update:modelValue", e.target.value);
    };
    watch(
      () => props.modelValue,
      (value) => {
        el.value.style.height = "40px";
        if (value) {
          el.value.style.height = el.value.scrollHeight + "px";
        }
      }
    );
    const submit = (e) => {
      if (!e.shiftKey) {
        e.preventDefault();
        emit("submit");
      }
    };
    return { el, handleInput, submit };
  },
};
</script>

<style scoped>
textarea {
  padding: 8px;
  resize: none;
}
textarea[rows="1"] {
  height: 40px;
}
</style>