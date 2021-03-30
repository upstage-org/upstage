<template>
  <RadioGroup
    title="Type"
    v-model="mediaType"
    :data="['avatar', 'prop', 'backdrop', 'audio', 'stream']"
    :render-label="titleCase"
    allow-clear
    clear-tooltip="Media without type cannot be attach to a stage, but can be use to compose to other media, like multiframes avatar"
  />
</template>

<script>
import { ref } from "@vue/reactivity";
import { watchEffect } from "@vue/runtime-core";
import RadioGroup from "./RadioGroup";
import { titleCase } from "@/utils/common";

export default {
  props: ["modelValue"],
  emits: ["update:modelValue"],
  components: { RadioGroup },
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
  methods: { titleCase },
};
</script>

<style>
</style>