<template>
  <div class="file">
    <label class="file-label">
      <input
        class="file-input"
        type="file"
        name="resume"
        :accept="accept"
        @input="handleInputFile"
      />
      <span class="file-cta">
        <span class="file-icon">
          <i class="fas fa-upload"></i>
        </span>
        <span class="file-label"> Choose a file… </span>
      </span>
      <div class="mt-2 mx-2">
        <div v-if="unlimit">No size limit</div>
        <div v-else :class="{ 'has-text-danger': file?.size > mediaLimit }">
          <span>Maximum file size: {{ humanFileSize(mediaLimit) }}&nbsp;</span>
          <span v-if="file">
            <i class="fas fa-times" v-if="file.size > mediaLimit"></i>
            <i class="fas fa-check" v-else></i>
            (current size: {{ humanFileSize(file.size) }})
          </span>
        </div>
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
import { computed, watch } from "@vue/runtime-core";
import { humanFileSize } from "@/utils/common";
import { useStore } from "vuex";
export default {
  props: {
    modelValue: String,
    unlimit: Boolean,
    acceptImage: {
      type: Boolean,
      default: true,
    },
    acceptAudio: {
      type: Boolean,
      default: false,
    },
    acceptVideo: {
      type: Boolean,
      default: false,
    },
  },
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
      if (file.value.size <= mediaLimit.value || props.unlimit) {
        emit("change", file.value);
      } else {
        emit("change", null);
      }
    };
    const accept = computed(() => {
      let extensions = [];
      if (props.acceptImage) {
        extensions.push("image/*");
      }
      if (props.acceptAudio) {
        extensions.push("audio/mp3,audio/*");
      }
      if (props.acceptVideo) {
        extensions.push("video/mp4,video/x-m4v,video/*");
      }
      return extensions.join(",");
    });

    watch(
      () => props.unlimit,
      () => {
        file.value = null;
        emit("change", null);
      }
    );

    const isImage = computed(() => file.value?.type?.startsWith("image"));

    return {
      handleInputFile,
      file,
      isImage,
      mediaLimit,
      humanFileSize,
      accept,
    };
  },
};
</script>

<style>
</style>