<template>
  <Modal v-model="active">
    <template #trigger>
      <button class="button">
        <span class="icon">
          <i class="fas fa-plus"></i>
        </span>
        <span>New</span>
      </button>
    </template>
    <template #header>Upload Media</template>
    <template #content>
      <HorizontalField title="Media Name">
        <Field
          v-model="data.name"
          help="Leave blank for default filename"
          @blur="handleBlurName"
        />
      </HorizontalField>
      <MediaType v-model="data.mediaType" />
      <HorizontalField title="Attachment">
        <Upload
          v-model="data.base64"
          @change="
            data.file = $event;
            handleBlurName();
          "
          :unlimit="data.mediaType === 'stream'"
          :accept-image="
            ['avatar', 'prop', 'backdrop', null].includes(data.mediaType)
          "
          :accept-audio="['audio', null].includes(data.mediaType)"
          :accept-video="['stream', null].includes(data.mediaType)"
        />
      </HorizontalField>
    </template>
    <template #footer>
      <SaveButton @click="upload" :loading="loading" :disabled="!data.file" />
    </template>
  </Modal>
</template>

<script>
import Modal from "./Modal.vue";
import SaveButton from "./form/SaveButton";
import HorizontalField from "./form/HorizontalField";
import MediaType from "./form/MediaType";
import Field from "./form/Field";
import Upload from "./form/Upload";
import { reactive, ref } from "@vue/reactivity";
import { useMutation } from "@/services/graphql/composable";
import { stageGraph } from "@/services/graphql";
import { notification } from "@/utils/notification";

export default {
  components: { Modal, SaveButton, HorizontalField, Field, Upload, MediaType },
  emits: ["complete"],
  setup: (props, { emit }) => {
    const active = ref();
    const data = reactive({});

    const handleBlurName = () => {
      if (!data.name) {
        data.name = data.file?.name;
      }
    };

    const { loading, mutation } = useMutation(stageGraph.uploadMedia);
    const upload = async () => {
      try {
        const { name, base64, mediaType } = data;
        const response = await mutation({
          name,
          base64,
          mediaType,
          filename: data.file.name,
        });
        active.value = false;
        notification.success("Media uploaded successfully!");
        emit("complete", response);
        data.name = data.base64 = data.mediaType = data.filename = data.file = null;
      } catch (error) {
        notification.error(error);
      }
    };

    return {
      loading,
      upload,
      data,
      active,
      handleBlurName,
    };
  },
};
</script>

<style>
</style>