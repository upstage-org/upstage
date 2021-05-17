<template>
  <Upload
    v-if="!active && !loading"
    v-model="base64"
    @change="handleFileChange"
  >
    <span class="icon">
      <i class="fas fa-plus"></i>
    </span>
    <span>New</span>
  </Upload>
  <Modal width="100%" v-model="active">
    <template #header>Upload Media</template>
    <template #content>
      <MediaForm v-if="media" :media="media" />
      <Skeleton v-else-if="loading" />
    </template>
  </Modal>
</template>

<script>
import Modal from "@/components/Modal.vue";
import Upload from "@/components/form/Upload";
import Skeleton from "@/components/Skeleton";
import MediaForm from "./MediaForm";
import { ref } from "@vue/reactivity";
import { useMutation } from "@/services/graphql/composable";
import { stageGraph } from "@/services/graphql";
import { notification } from "@/utils/notification";

export default {
  components: { Modal, MediaForm, Upload, Skeleton },
  emits: ["complete"],
  setup: (props, { emit }) => {
    const base64 = ref();
    const active = ref();
    const { loading, mutation } = useMutation(stageGraph.uploadMedia);

    const media = ref();

    const getType = (fileType) => {
      if (fileType === "image") return "avatar";
      if (fileType === "audio") return "audio";
      if (fileType === "video") return "stream";
    };

    const handleFileChange = async (file, type) => {
      if (!file) return;
      try {
        active.value = true;
        const response = await mutation({
          name: file.name,
          base64: base64.value,
          mediaType: getType(type),
          filename: file.name,
        });
        if (response) {
          media.value = response.uploadMedia.asset;
          notification.success("Media uploaded successfully!");
          emit("complete", response);
        }
      } catch (error) {
        notification.error(error);
        active.value = false;
      }
    };

    return {
      loading,
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