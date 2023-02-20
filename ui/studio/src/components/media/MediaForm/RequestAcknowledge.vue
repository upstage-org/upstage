<script lang="ts" setup>
import { message } from "ant-design-vue";
import { PropType, inject } from "vue";
import { Media } from "../../../models/studio";
import { useRequestPermission } from "./composable";

const props = defineProps({
  media: {
    type: Object as PropType<Media>,
    required: true,
  },
});

const refresh = inject("refresh", () => {});
const { mutate, loading } = useRequestPermission();
const sendAcknowledge = async () => {
  const response = await mutate({
    assetId: props.media.id,
  });
  if (response?.data?.requestPermission.success) {
    message.success("Acknowledge sent! Enjoy using " + props.media.name + "!");
    refresh();
  }
};
</script>

<template>
  <a-tooltip placement="left">
    <template #title>
      By clicking the button, you acknowledge that you are using the media
      created by
      <DName :user="media.owner" />
    </template>
    <smart-button type="dashed" :action="sendAcknowledge">
      <CheckSquareOutlined />Acknowledge
    </smart-button>
  </a-tooltip>
</template>
