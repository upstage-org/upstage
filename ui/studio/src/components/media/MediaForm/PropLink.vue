<script lang="ts" setup>
import { PropType } from "vue";
import { Link } from "../../../models/studio";

const props = defineProps({
  link: {
    type: Object as PropType<Link>,
    required: true,
  },
});
</script>

<template>
  <a-space direction="vertical" class="w-full mb-4">
    <a-form-item label="URL" :labelCol="{ span: 6 }" class="mb-2">
      <a-input
        placeholder="The destination when audience click on the link"
        v-model:value="props.link.url"
      />
    </a-form-item>
    <a-form-item label="Open in new tab" :labelCol="{ span: 6 }" class="mb-2">
      <a-switch v-model:checked="props.link.blank" />
    </a-form-item>
    <a-form-item label="Hover effect" :labelCol="{ span: 6 }" class="mb-2">
      <a-switch v-model:checked="props.link.effect" />
    </a-form-item>
  </a-space>
</template>
