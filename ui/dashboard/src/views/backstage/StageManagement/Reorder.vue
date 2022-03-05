<template>
    <div v-for="mediaType in types" :key="mediaType">
        <h4 class="subtitle">{{ mediaType }}</h4>
    </div>
</template>

<script setup>
import { defineProps, defineEmits, computed } from 'vue';

const props = defineProps({
    modelValue: {
        type: Array,
        required: true,
    },
})

defineEmits(['update:modelValue'])

const types = computed(() => [...new Set(props.modelValue.map(media => media.mediaType))])
</script>

<style>
.subtitle {
    text-transform: capitalize;
}
</style>