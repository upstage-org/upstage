<script setup>
import LarixQRCode from "components/LarixQRCode.vue";
import QRCode from "components/QRCode.vue";
import Modal from "components/Modal.vue";
import { getPublishLink } from "utils/streaming";
import { defineProps, watch } from "vue";
import { useQuery } from "services/graphql/composable";
import { stageGraph } from "services/graphql";
import modernCopy from "modern-copy";
import { message } from "ant-design-vue";
import OBSInstruction from "./OBSInstruction.vue";

const props = defineProps({
  stream: Object,
});

const { data } = useQuery(stageGraph.getStreamSign, props.stream.url);
watch(
  data,
  (sign) => {
    Object.assign(props.stream, { sign });
  },
  { immediate: true },
);

const copyLink = () => {
  const link = `${getPublishLink(props.stream.url)}?sign=${props.stream.sign}`;
  modernCopy(link);
  message.success(`${link} copied to clipboard!`);
};
</script>

<template>
  <Modal width="336px">
    <template #trigger>
      <QRCode :value="stream.name" :size="42" type="svg" />
      <span class="tag is-light is-block">{{ stream.name }}</span>
    </template>
    <template #content>
      <a-tooltip title="Click to copy link">
        <LarixQRCode :stream="stream" @click="copyLink" class="has-tooltip-bottom" />
      </a-tooltip>
      <p class="has-text-centered">
        Scan the above QR Code to start streaming with Larix, or follow this
        instruction if you're using OBS Studio:
        <OBSInstruction :url="stream.url" :sign="stream.sign" />
      </p>
    </template>
  </Modal>
</template>

<style></style>
