<template>
  <Dropdown
    title="Type"
    v-model="mediaType"
    :data="data ?? ['avatar', 'prop', 'backdrop', 'audio', 'stream', 'curtain']"
    :render-label="titleCase"
    :is-up="isUp"
  />
</template>

<script>
import { ref } from "vue";
import { watchEffect } from "vue";
import Dropdown from "./Dropdown.vue";
import { titleCase } from "utils/common";

export default {
  props: ["modelValue", "isUp", "data"],
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

<style></style>
