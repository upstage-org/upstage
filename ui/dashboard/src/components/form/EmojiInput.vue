<template>
  <input
    v-if="!pickerOnly"
    ref="input"
    class="input is-rounded"
    v-bind="$attrs"
    :value="modelValue"
    @input="$emit('update:modelValue', $event.target.value)"
  />
  <div v-click-outside="() => (isPicking = false)" style="display: inline">
    <button
      type="button"
      class="icon is-right clickable button is-rounded"
      :class="{
        'is-loading': loading,
        'is-primary': !className,
        [className]: true,
      }"
      :disabled="loading"
      :style="style"
      @click="isPicking = !isPicking"
    >
      <slot name="icon">
        <i class="far fa-smile"></i>
      </slot>
    </button>
    <transition :css="false" @enter="pickerEnter">
      <emoji-picker v-show="isPicking" class="light" />
    </transition>
  </div>
</template>

<script>
import "emoji-picker-element";
import { ref } from "vue";
import anime from "animejs";

export default {
  props: ["loading", "modelValue", "pickerOnly", "style", "className"],
  emits: ["update:modelValue"],
  setup: (props, { emit }) => {
    const input = ref();
    const isPicking = ref(false);

    const handleEmoji = ({ detail: { unicode } }) => {
      if (props.pickerOnly) {
        emit("update:modelValue", unicode);
      } else {
        const start = input.value.selectionStart;
        const end = input.value.selectionEnd;
        const value = props.modelValue ?? "";
        emit(
          "update:modelValue",
          `${value.substring(0, start)}${unicode}${value.substring(
            end,
            value.length
          )}`
        );
      }
    };
    const pickerEnter = (el, complete) => {
      el.addEventListener("emoji-click", handleEmoji);
      anime({
        targets: el,
        scaleX: [0, 1],
        scaleY: [0, 1],
        duration: 500,
        complete,
      });
    };
    return { input, isPicking, pickerEnter };
  },
};
</script>

<style scoped lang="scss">
emoji-picker {
  --border-size: 0.5px;
  --outline-size: 0;
  --input-border-radius: 24px;
  --input-border-color: #b5b5b5;

  position: absolute;
  bottom: 40px;
  right: 0;
  z-index: 1000;
  overflow: hidden;
  border-radius: 8px;
  box-shadow: 0 0.5em 1em -0.125em rgba(10, 10, 10, 0.1),
    0 0px 0 1px rgba(10, 10, 10, 0.02);
  transform-origin: bottom right;
}
</style>