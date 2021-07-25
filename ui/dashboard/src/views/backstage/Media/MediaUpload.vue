<template>
  <div class="dropdown is-hoverable">
    <div class="dropdown-trigger">
      <Upload v-if="!active" v-model="base64" @change="handleFileChange">
        <span>New</span>
        <span class="icon">
          <i class="fas fa-plus"></i>
        </span>
      </Upload>
    </div>
    <div v-if="special" class="dropdown-menu" role="menu">
      <div class="dropdown-content">
        <div class="dropdown-item">
          <p>Special media that does not require upload:</p>
        </div>
        <hr class="dropdown-divider" />
        <a class="dropdown-item" @click="newRTMPStream">
          <span class="icon">
            <i class="fas fa-video"></i>
          </span>
          <span>RTMP Stream</span>
        </a>
      </div>
    </div>
  </div>
  <Modal width="100%" height="100%" v-model="active">
    <MediaForm v-if="media" :media="media" @complete="uploadCompleted" />
  </Modal>
</template>

<script>
import Modal from "@/components/Modal.vue";
import Upload from "@/components/form/Upload";
import MediaForm from "./MediaForm";
import { ref } from "@vue/reactivity";
import { inject } from "@vue/runtime-core";
import { getUniqueKey } from "@/utils/streaming";

export default {
  props: ["special"],
  components: { Modal, MediaForm, Upload },
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
      if (file) {
        active.value = true;
        media.value = {
          name: file.name,
          base64: base64.value,
          mediaType: getType(type),
          fileType: type,
          filename: file.name,
          stages: [],
        };
      }
    };

    const refresh = inject("refresh");
    const uploadCompleted = () => {
      refresh();
      media.value = null;
    };

    const newRTMPStream = () => {
      media.value = {
        name: "",
        base64: "",
        filename: "stream.rtmp",
        mediaType: "stream",
        stages: [],
        isRTMP: true,
        src: getUniqueKey(),
      };
      active.value = true;
    };

    return {
      active,
      base64,
      media,
      handleFileChange,
      uploadCompleted,
      newRTMPStream,
    };
  },
};
</script>

<style>
</style>