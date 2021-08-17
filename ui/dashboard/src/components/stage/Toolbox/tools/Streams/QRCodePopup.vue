<script setup>
import OBSInstruction from "@/views/backstage/Media/OBSInstruction";
import LarixQRCode from "@/components/LarixQRCode";
import QRCode from "@/components/QRCode";
import Modal from "@/components/Modal";
import { defineProps, watch } from "vue";
import { useQuery } from "@/services/graphql/composable";
import { stageGraph } from "@/services/graphql";

const props = defineProps({
  stream: Object,
});

const { data } = useQuery(stageGraph.getStreamSign, props.stream.url);
watch(
  data,
  (sign) => {
    Object.assign(props.stream, { sign });
  },
  { immediate: true }
);
</script>

<template>
  <Modal width="336px">
    <template #trigger>
      <QRCode :value="stream.name" :size="42" type="svg" />
      <span class="tag is-light is-block">{{ stream.name }}</span>
    </template>
    <template #content>
      <LarixQRCode :stream="stream" />
      <p class="has-text-centered">
        Or follow this instruction if you're using OBS Studio:
        <OBSInstruction :url="stream.url" :sign="stream.sign" />
      </p>
    </template>
  </Modal>
</template>

<style>
</style>