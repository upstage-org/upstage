<template>
  <RTMPStream controls :src="media.src" />
  <Field
    horizontal
    label="Unique key"
    :modelValue="modelValue"
    @update:modelValue="$emit('update:modelValue', $event)"
    help="You can change it to anything you like, but remember: it must be unique!"
  />
  <p>
    Use this URL to publish your stream:
    <a :href="getPublishLink(modelValue)">{{ getPublishLink(modelValue) }}</a>
  </p>
  <OBSInstruction :src="modelValue" />
  <QRCode value="Alo" />
</template>

<script>
import Field from "@/components/form/Field";
import RTMPStream from "@/components/RTMPStream";
import OBSInstruction from "./OBSInstruction";
import { getPublishLink } from "@/utils/streaming";
import QRCode from "@/components/QRCode";

export default {
  props: ["modelValue", "media"],
  emits: ["update:modelValue"],
  components: { Field, RTMPStream, OBSInstruction, QRCode },
  methods: {
    getPublishLink,
  },
};
</script>

<style>
</style>