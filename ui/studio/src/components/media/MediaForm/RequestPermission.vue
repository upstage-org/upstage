<script lang="ts" setup>
import { message } from "ant-design-vue";
import { PropType, ref, inject } from "vue";
import { Media } from "models/studio";
import { absolutePath } from "utils/common";
import { useRequestPermission } from "./composable";

const props = defineProps({
  media: {
    type: Object as PropType<Media>,
    required: true,
  },
});

const visible = ref(false);
const note = ref("");

const refresh = inject("refresh", () => {});
const { mutate, loading } = useRequestPermission();
const handleOk = async () => {
  if (!note.value.trim()) {
    message.warning("Please provide a reason!");
    return;
  }
  const response = await mutate({
    assetId: props.media.id,
    note: note.value,
  });
  if (response?.data?.requestPermission.success) {
    message.success("Permission request sent");
    visible.value = false;
    refresh();
  }
};
</script>

<template>
  <a-button type="dashed" @click="visible = true">
    <SendOutlined />Request permission
  </a-button>
  <a-modal
    v-model:visible="visible"
    :confirm-loading="loading"
    @ok="handleOk"
    okText="Send Request"
  >
    You are requesting permission for
    <a-avatar class="my-2" :src="absolutePath(media.src)" />
    {{ media.name }}.
    <a-textarea
      v-model:value="note"
      :placeholder="`Please write something so that ${media.owner.username} can understand more about your purpose of using the media...`"
      :auto-size="{ minRows: 2, maxRows: 5 }"
    />
  </a-modal>
</template>
