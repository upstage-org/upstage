<script setup>
import { ref, watchEffect } from "@vue/runtime-core";
import QRCodeStyling from "qr-code-styling";
import { defineProps } from "vue";
import upstage from "@/assets/upstage.png";

const props = defineProps({
  value: String,
  size: {
    type: Number,
    default: 128,
  },
});

const el = ref();

const qrCode = new QRCodeStyling({
  width: props.size,
  height: props.size,
  type: "svg",
  data: props.value,
  image: upstage,
  dotsOptions: {
    type: "rounded",
  },
});

watchEffect(() => {
  qrCode.update({
    data: props.value,
  });

  qrCode.append(el.value);
});
</script>

<template>
  <div ref="el"></div>
</template>

<style>
</style>