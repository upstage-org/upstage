<script lang="ts" setup>
import { computed } from "vue";
import moment from "moment";
import { Tooltip } from "ant-design-vue";

const { value } = defineProps({
  value: Date,
});

const text = computed(() => moment.utc(value).fromNow());
const localFormatted = computed(() => moment(value).format("lll"));
</script>

<template>
  <Tooltip :title="localFormatted" class="cursor-help">
    {{ text }}
  </Tooltip>
</template>
