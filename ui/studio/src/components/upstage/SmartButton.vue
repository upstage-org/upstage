<script lang="ts" setup>
import { message } from 'ant-design-vue';
import { ref, PropType } from 'vue';

const props = defineProps({
  action: {
    type: Function as PropType<(e?: any) => Promise<any>>,
    required: true,
  }
});
const loading = ref(false);
const handleClick = async (e: any): Promise<void> => {
  try {
    loading.value = true;
    await props.action(e);
    loading.value = false;
  } catch (error: any) {
    message.error(error.message ? error.message : error);
  }
};
</script>

<template>
  <a-button v-bind="$attrs" @click="handleClick" :loading="loading">
    <slot />
  </a-button>
</template>