<script setup>
import { onMounted, ref, watchEffect } from "vue";
import QRCodeStyling from "qr-code-styling";
import upstage from "../../assets/upstage.png";

const props = defineProps({
    value: String,
    size: {
        type: Number,
        default: 300,
    },
    type: {
        type: String,
        default: "canvas",
    },
});

const el = ref();

const qrCode = new QRCodeStyling({
    width: props.size,
    height: props.size,
    data: props.value,
    type: props.type,
    image: upstage,
    dotsOptions: {
        type: "rounded",
    },
});

onMounted(() => {
    qrCode.append(el.value);
});

watchEffect(() => {
    qrCode.update({
        data: props.value,
    });
});
</script>

<template>
    <div class="qr-code" ref="el"></div>
</template>

<style scoped lang="less">
.qr-code {
    text-align: center;

    ::v-deep(canvas) {
        border-radius: 8px;
    }
}
</style>