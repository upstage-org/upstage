<script lang="ts" setup>
import { computed } from "vue";
import moment from "moment";

const { value } = defineProps({
  value: Date,
});

const text = computed(() => moment.utc(value).fromNow());
</script>

<template>
  {{ text }}
</template>
