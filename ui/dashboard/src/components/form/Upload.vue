<template>
  <div class="file">
    <label class="file-label">
      <input
        class="file-input"
        type="file"
        name="resume"
        @input="handleInputFile"
      />
      <span class="file-cta">
        <span class="file-icon">
          <i class="fas fa-upload"></i>
        </span>
        <span class="file-label"> Choose a file… </span>
      </span>
      <div class="mt-2 mx-2 has-text-danger" v-if="file?.size > mediaLimit">
        Media needs to be no bigger than
        {{ humanFileSize(mediaLimit) }} (current size:
        {{ humanFileSize(file?.size) }})
      </div>
    </label>
  </div>
  <p class="help">
    <img v-if="isImage" :src="modelValue" alt="Preview" />
    <b v-else>{{ file?.name }}</b>
  </p>
</template>

<script>
import { ref } from "@vue/reactivity";
import { computed } from "@vue/runtime-core";
import { humanFileSize } from "@/utils/common";
import { useStore } from "vuex";
export default {
  props: ["modelValue"],
  emits: ["update:modelValue", "change"],
  setup: (props, { emit }) => {
    const store = useStore();
    const mediaLimit = computed(
      () => store.state.user.user?.uploadLimit ?? 1024 * 1024
    );
    const file = ref();
    const handleInputFile = (e) => {
      const reader = new FileReader();
      reader.readAsDataURL(e.target.files[0]);
      reader.onload = () => {
        emit("update:modelValue", reader.result);
      };
      file.value = e.target.files[0];
      if (file.value.size <= mediaLimit.value) {
        emit("change", file.value);
      } else {
        emit("change", null);
      }
    };

    const isImage = computed(() => file.value?.type?.startsWith("image"));

    return { handleInputFile, file, isImage, mediaLimit, humanFileSize };
  },
};
</script>

<style>
</style>