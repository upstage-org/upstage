<script lang="ts" setup>
import { message } from "ant-design-vue";
import modernCopy from "modern-copy";

const props = defineProps({
    value: { type: String, required: true },
});
const copy = () => {
    modernCopy(props.value);
    message.success(`${props.value} copied to clipboard!`);
};
</script>

<template>
    <code class="bg-gray-200 text-red-600 p-1 text-sm">{{ value }}</code>
    <a-tooltip title="Copy to clipboard">
        <code @click="copy" class="bg-gray-800 text-red-600 text-sm px-2 py-1 cursor-pointer">
            <copy-outlined />
        </code>
    </a-tooltip>
</template>