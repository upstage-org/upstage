<script lang="ts" setup>
import { ref } from '@vue/reactivity';
import configs from '../config';
import { getSharedAuth } from '../utils/common';

const auth = ref<{ refresh_token: string, token: string }>()

const sharedState = getSharedAuth()
auth.value = sharedState

</script>

<template>
  <slot v-if="auth"></slot>
  <a-result
    v-else
    status="403"
    title="UpStage Player Required"
    sub-title="Sorry, you are not authorized to access this page."
  >
    <template #extra>
      <a :href="configs.UPSTAGE_URL ?? '/backstage'">
        <a-button type="primary">Login</a-button>
      </a>
    </template>
  </a-result>
</template>