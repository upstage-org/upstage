<script lang="ts" setup>
import { computed } from '@vue/reactivity';
import moment from 'moment'

const { value } = defineProps({
  value: Date
})

const text = computed(() => moment(value).fromNow())
</script>

<template>{{ text }}</template>