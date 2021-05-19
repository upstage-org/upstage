<template>
  <Upload v-if="!active" v-model="base64" @change="handleFileChange">
    <span class="icon">
      <i class="fas fa-plus"></i>
    </span>
    <span>New</span>
  </Upload>
  <Modal width="100%" height="100%" v-model="active">
    <MediaForm
      v-if="media"
      :media="media"
      @complete="$emit('complete', $event)"
    />
  </Modal>
</template>

<script>
import Modal from "@/components/Modal.vue";
import Upload from "@/components/form/Upload";
import MediaForm from "./MediaForm";
import { ref } from "@vue/reactivity";

export default {
  components: { Modal, MediaForm, Upload },
  emits: ["complete"],
  setup: () => {
    const base64 = ref();
    const active = ref();

    const media = ref();

    const getType = (fileType) => {
      if (fileType === "image") return "avatar";
      if (fileType === "audio") return "audio";
      if (fileType === "video") return "stream";
    };

    const handleFileChange = async (file, type) => {
      active.value = true;
      media.value = {
        name: file.name,
        base64: base64.value,
        mediaType: getType(type),
        filename: file.name,
        stages: [],
      };
    };

    return {
      active,
      base64,
      media,
      handleFileChange,
    };
  },
};
</script>

<style>
</style>