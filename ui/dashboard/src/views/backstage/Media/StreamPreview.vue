<template>
  <RTMPStream controls :src="media.src" />
  <Field
    horizontal
    label="Unique key"
    :modelValue="modelValue"
    @update:modelValue="$emit('update:modelValue', $event)"
    help="You can change it to anything you like, but remember: it must be unique!"
  />
  <div class="columns">
    <div class="column">
      Scan this QR Code to start streaming with Larix Broadcaster
      <QRCode :value="code" :size="300" />
    </div>
    <div class="column">
      Or follow this instruction to start streaming with OBS Studio
      <OBSInstruction :src="modelValue" />
    </div>
  </div>
</template>

<script>
import Field from "@/components/form/Field";
import RTMPStream from "@/components/RTMPStream";
import OBSInstruction from "./OBSInstruction";
import { getLarixLink, getPublishLink } from "@/utils/streaming";
import QRCode from "@/components/QRCode";
import { computed } from "@vue/reactivity";

export default {
  props: ["modelValue", "media"],
  emits: ["update:modelValue"],
  components: { Field, RTMPStream, OBSInstruction, QRCode },
  methods: {
    getPublishLink,
  },
  setup: (props) => {
    const code = computed(() => getLarixLink(props.modelValue));

    return { code };
  },
};
</script>

<style>
</style>