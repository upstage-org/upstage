<script setup lang="ts">
import { ref, provide } from 'vue';
import configs from '../../config';
import { UploadFile } from '../../models/studio';

const visible = ref(false)
const files = ref<UploadFile[]>([])
const composingMode = ref(false)
provide('composingMode', composingMode)
provide('files', files)
provide('visibleDropzone', visible)

window.addEventListener('dragenter', e => {
  e.preventDefault()
  visible.value = true
})

const toSrc = ({ file }: { file: File }) => {
  return URL.createObjectURL(file)
}

const handleUpload = (file: any) => {
  files.value = files.value.concat({
    ...file,
    id: files.value.length,
    preview: toSrc(file),
    status: 'local'
  })
  visible.value = false
}
</script>

<template>
  <a-modal :footer="null" :visible="visible" @cancel="visible = false" width="100%" wrapClassName="fullscreen-dragzone"
    class="h-full top-0 p-0">
    <a-upload-dragger :show-upload-list="false" :custom-request="handleUpload" multiple>
      <p class="ant-upload-drag-icon">
        <UploadOutlined />
      </p>
      <p class="ant-upload-text">{{ $t("upload_hint") }}</p>
      <p class="ant-upload-hint">
        {{
            $t("upload_accepted_format", {
              image: configs.ALLOWED_EXTENSIONS.IMAGE,
              audio: configs.ALLOWED_EXTENSIONS.AUDIO,
              video: configs.ALLOWED_EXTENSIONS.VIDEO
            })
        }}
      </p>
    </a-upload-dragger>
  </a-modal>
  <slot></slot>
</template>

<style lang="less">
.fullscreen-dragzone {
  z-index: 999999;

  .ant-modal-content {
    height: 100%;
  }

  .ant-modal-body {
    padding: 0;
    height: 100%;
  }
}
</style>