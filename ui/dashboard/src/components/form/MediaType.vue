<template>
  <HorizontalField title="Type">
    <div class="control">
      <label class="radio">
        <input type="radio" v-model="mediaType" value="avatar" />
        Avatar
      </label>
      <label class="radio">
        <input type="radio" v-model="mediaType" value="prop" />
        Prop
      </label>
      <label class="radio">
        <input type="radio" v-model="mediaType" value="backdrop" />
        Backdrop
      </label>
      <label class="radio">
        <input type="radio" v-model="mediaType" value="audio" />
        Audio
      </label>
      <label class="radio">
        <input type="radio" v-model="mediaType" value="stream" />
        Stream
      </label>
      <button
        v-if="mediaType"
        @click="mediaType = null"
        class="button is-danger ml-2 is-small"
        data-tooltip="Media without type cannot be attach to a stage, but can be use to compose to other media, like multiframes avatar"
      >
        <span class="icon">
          <i class="fas fa-times"></i>
        </span>
        <span> Clear </span>
      </button>
    </div>
  </HorizontalField>
</template>

<script>
import { ref } from "@vue/reactivity";
import { watchEffect } from "@vue/runtime-core";
import HorizontalField from "./HorizontalField";

export default {
  props: ["modelValue"],
  emits: ["update:modelValue"],
  components: { HorizontalField },
  setup: (props, { emit }) => {
    const mediaType = ref();
    watchEffect(() => {
      emit("update:modelValue", mediaType.value);
    });
    watchEffect(() => {
      if (props.modelValue === "media") {
        mediaType.value = null;
      } else {
        mediaType.value = props.modelValue;
      }
    });

    return { mediaType };
  },
};
</script>

<style>
</style>