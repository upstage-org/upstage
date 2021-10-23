<script setup lang="ts">
import { ref, reactive, provide } from 'vue';
import configs from '../../config';

const visible = ref(false)
const files = reactive<any>([])
provide('files', files)
provide('visibleDropzone', visible)

window.addEventListener('dragenter', e => {
  e.preventDefault()
  visible.value = true
})

const handleUpload = (file: any) => {
  files.push(file)
  visible.value = false
}
</script>

<template>
  <a-modal
    :footer="null"
    :visible="visible"
    @cancel="visible = false"
    width="100%"
    class="fullscreen-dragzone"
  >
    <a-upload-dragger :show-upload-list="false" :custom-request="handleUpload" multiple>
      <p class="ant-upload-drag-icon">
        <UploadOutlined />
      </p>
      <p
        class="ant-upload-text"
      >Drag files here to upload. You can drop multiple files to make a multiframes media</p>
      <p
        class="ant-upload-hint"
      >Accepted file formats: {{ configs.ALLOWED_EXTENSIONS.IMAGE }} for images, {{ configs.ALLOWED_EXTENSIONS.AUDIO }} for audios and {{ configs.ALLOWED_EXTENSIONS.VIDEO }} for videos</p>
    </a-upload-dragger>
  </a-modal>
  <slot></slot>
</template>

<style lang="less">
.fullscreen-dragzone {
  height: 100%;
  top: 0;
  padding-bottom: 0;
  z-index: 99999;
  .ant-modal-content {
    height: 100%;
  }
  .ant-modal-body {
    padding: 0;
    height: 100%;
  }
}
</style>