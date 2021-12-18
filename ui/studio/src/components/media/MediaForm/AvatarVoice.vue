<script lang="ts" setup>
import { reactive } from 'vue';
import { AvatarVoice } from '../../../models/studio';
import { getVoiceList, getVariantList, getDefaultVariant } from '../../../services/speech/voice'

const av = reactive<AvatarVoice>({
  voice: null,
  variant: getDefaultVariant(),
  pitch: 50,
  speed: 50,
  amplitude: 50,
})
</script>

<template>
  <a-form-item label="Voice" :labelCol="{ span: 3 }" class="mb-2">
    <a-select v-model:value="av.voice" placeholder="No voice" :options="getVoiceList()" allowClear />
  </a-form-item>
  <a-form-item label="Variant" :labelCol="{ span: 3 }" class="mb-2">
    <a-select v-model:value="av.variant" :options="getVariantList()" />
  </a-form-item>
  <a-form-item label="Pitch" :labelCol="{ span: 3 }" class="mb-2">
    <a-slider v-model:value="av.pitch" />
  </a-form-item>
  <a-form-item label="Rate" :labelCol="{ span: 3 }" class="mb-2">
    <a-slider v-model:value="av.speed" />
  </a-form-item>
  <a-form-item label="Volume" :labelCol="{ span: 3 }" class="mb-2">
    <a-slider v-model:value="av.amplitude" />
  </a-form-item>
  <a-form-item label="Test voice" :labelCol="{ span: 3 }" class="mb-2">
    <a-input-search placeholder="Welcome to UpStage!">
      <template #enterButton>
        <sound-outlined />
      </template>
    </a-input-search>
  </a-form-item>
</template>