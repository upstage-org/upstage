<template>
  <Dropdown
    title="Type"
    v-model="mediaType"
    :data="['avatar', 'prop', 'backdrop', 'audio', 'stream']"
    :render-label="titleCase"
  />
</template>

<script>
import { ref } from "@vue/reactivity";
import { watchEffect } from "@vue/runtime-core";
import Dropdown from "./Dropdown";
import { titleCase } from "@/utils/common";

export default {
  props: ["modelValue"],
  emits: ["update:modelValue"],
  components: { Dropdown },
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