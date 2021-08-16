<script setup>
import QRCodeStyling from "qr-code-styling";
const { onMounted, ref } = require("@vue/runtime-core");

const props = defineProps({
  value: String,
});

const el = ref();

onMounted(() => {
  console.log("qr code");
  const qrCode = new QRCodeStyling({
    width: 300,
    height: 300,
    type: "svg",
    data: props.value,
    image:
      "https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg",
    dotsOptions: {
      type: "rounded",
    },
  });

  qrCode.append(document.getElementById("canvas"));
  qrCode.download({ name: "qr", extension: "svg" });
});
</script>

<template>
  <div ref="el"></div>
</template>

<style>
</style>