<template>
  <Modal :active="active">
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
      <HorizontalField title="Type">
        <div class="control">
          <label class="radio">
            <input type="radio" v-model="data.mediaType" value="avatar" />
            Avatar
          </label>
          <label class="radio">
            <input type="radio" v-model="data.mediaType" value="prop" />
            Prop
          </label>
          <label class="radio">
            <input type="radio" v-model="data.mediaType" value="backdrop" />
            Backdrop
          </label>
          <label class="radio">
            <input type="radio" v-model="data.mediaType" value="audio" />
            Audio
          </label>
        </div>
      </HorizontalField>
      <HorizontalField title="Attachment">
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
          </label>
        </div>
        <p class="help">
          <img v-if="isImage" :src="data.base64" alt="Preview" />
          <b v-else>{{ data.file?.name }}</b>
        </p>
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
import Field from "./form/Field";
import { reactive, ref } from "@vue/reactivity";
import { computed } from "@vue/runtime-core";
import { useMutation } from "@/services/graphql/composable";
import { stageGraph } from "@/services/graphql";
import { notification } from "@/utils/notification";

export default {
  components: { Modal, SaveButton, HorizontalField, Field },
  emits: ["complete"],
  setup: (props, { emit }) => {
    const active = ref();
    const data = reactive({});

    const isImage = computed(() => data.file?.type?.startsWith("image"));

    const handleBlurName = () => {
      if (!data.name) {
        data.name = data.file?.name;
      }
    };

    const handleInputFile = (e) => {
      const reader = new FileReader();
      reader.readAsDataURL(e.target.files[0]);
      reader.onload = () => {
        data.base64 = reader.result;
      };
      data.file = e.target.files[0];
      handleBlurName();
    };

    const { loading, mutation } = useMutation(stageGraph.uploadMedia);
    const upload = async () => {
      try {
        const { name, base64, mediaType } = data;
        const response = await mutation({ name, base64, mediaType });
        active.value = false;
        notification.success("Media uploaded successfully!");
        emit("complete", response);
      } catch (error) {
        notification.error(error);
      }
    };

    return { isImage, handleInputFile, loading, upload, data, active };
  },
};
</script>

<style>
</style>