<template>
  <Field
    horizontal
    label="Unique key"
    :modelValue="modelValue"
    @update:modelValue="$emit('update:modelValue', trimKey($event))"
    :help="
      modelValue !== originalKey
        ? 'Stream key changed! Please save your stream before accessing it'
        : 'You can change it to anything you like, but remember: it must be unique!'
    "
  />
  <div v-if="modelValue === originalKey && media.sign" class="columns">
    <div class="column">
      Scan this QR Code to start streaming with Larix Broadcaster
      <LarixQRCode :stream="media" />
    </div>
    <div class="column">
      Or follow this instruction to start streaming with OBS Studio
      <OBSInstruction :url="modelValue" :sign="media.sign" />
    </div>
  </div>
  <RTMPStream v-if="media.id" controls :src="originalKey" />
</template>

<script>
import Field from "@/components/form/Field";
import RTMPStream from "@/components/RTMPStream";
import OBSInstruction from "./OBSInstruction";
import { getPublishLink } from "@/utils/streaming";
import LarixQRCode from "@/components/LarixQRCode";
import { ref } from "@vue/reactivity";

export default {
  props: ["modelValue", "media"],
  emits: ["update:modelValue"],
  components: { Field, RTMPStream, OBSInstruction, LarixQRCode },
  setup: (props) => {
    const originalKey = ref(props.media.src);
    const trimKey = (value) => value.replace(/\s/g, "").trim();
    return { getPublishLink, originalKey, trimKey };
  },
};
</script>

<style></style>
