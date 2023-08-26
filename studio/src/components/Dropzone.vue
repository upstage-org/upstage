<script setup lang="ts">
import { ref, provide } from "vue";
import configs from "config";
import { StudioGraph, UploadFile } from "models/studio";
import { message } from "ant-design-vue";
import { useQuery } from "@vue/apollo-composable";
import gql from "graphql-tag";
import { uploadDefault } from "models/studio";
import i18n from "../i18n";
import { humanFileSize } from "utils/common";

const { result } = useQuery<StudioGraph>(gql`
  query WhoAmI {
    whoami {
      username
      displayName
      roleName
      uploadLimit
    }
  }
`);

const visible = ref(false);
const files = ref<UploadFile[]>([]);
const composingMode = ref(false);
provide("composingMode", composingMode);
provide("files", files);
provide("visibleDropzone", visible);

window.addEventListener("dragenter", (e) => {
  e.preventDefault();
  visible.value = true;
});

const toSrc = ({ file }: { file: File }) => {
  return URL.createObjectURL(file);
};

const IsCanNotUpload = (size: number) => {
  let uploadLimit = result.value?.whoami.uploadLimit;

  if (uploadLimit) {
    return size <= uploadLimit ? false : true;
  }

  return size <= uploadDefault ? false : true;
};

const handleUpload = (file: any) => {
  let fileType = file.file.type;

  if (!fileType.includes("video") && IsCanNotUpload(file.file.size)) {
    message.error(
      i18n.global.t("over_limit_upload", {
        size: humanFileSize(file.file.size),
        limit: humanFileSize(result.value?.whoami.uploadLimit ?? 0),
      }),
    );
    return;
  }

  files.value = files.value.concat({
    ...file,
    id: files.value.length,
    preview: toSrc(file),
    status: "local",
  });
};

const uploadFile = (file: any) => {
  handleUpload(file);
  visible.value = false;
};
</script>

<template>
  <a-modal
    :footer="null"
    :visible="visible"
    @cancel="visible = false"
    width="100%"
    wrapClassName="fullscreen-dragzone"
    class="h-full top-0 p-0"
  >
    <a-upload-dragger
      :show-upload-list="false"
      :custom-request="uploadFile"
      multiple
    >
      <p class="ant-upload-drag-icon">
        <UploadOutlined />
      </p>
      <p class="ant-upload-text">{{ $t("upload_hint") }}</p>
      <p class="ant-upload-hint">
        {{
          $t("upload_accepted_format", {
            image: configs.ALLOWED_EXTENSIONS.IMAGE,
            audio: configs.ALLOWED_EXTENSIONS.AUDIO,
            video: configs.ALLOWED_EXTENSIONS.VIDEO,
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
