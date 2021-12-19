<script lang="ts" setup>
import { PropType, reactive, ref } from 'vue';
import { AvatarVoice } from '../../../models/studio';
import { avatarSpeak } from '../../../services/speech';
import { getVoiceList, getVariantList, getDefaultVariant } from '../../../services/speech/voice'

const props = defineProps({
  voice: {
    type: Object as PropType<AvatarVoice>,
    required: true
  }
})

const defaultTest = 'Welcome to UpStage!'
const test = ref('')
const testVoice = () => {
  avatarSpeak(props.voice, test.value || defaultTest)
}
</script>

<template>
  <a-form-item label="Voice" :labelCol="{ span: 3 }" class="mb-2">
    <a-select
      v-model:value="props.voice.voice"
      placeholder="No voice"
      :options="getVoiceList()"
      allowClear
    />
  </a-form-item>
  <template v-if="props.voice.voice">
    <a-form-item label="Variant" :labelCol="{ span: 3 }" class="mb-2">
      <a-select v-model:value="props.voice.variant" :options="getVariantList()" />
    </a-form-item>
    <a-form-item label="Pitch" :labelCol="{ span: 3 }" class="mb-2">
      <a-slider v-model:value="props.voice.pitch" />
    </a-form-item>
    <a-form-item label="Rate" :labelCol="{ span: 3 }" class="mb-2">
      <a-slider :value="props.voice.speed / 3.5" @change="props.voice.speed = $event * 3.5" />
    </a-form-item>
    <a-form-item label="Volume" :labelCol="{ span: 3 }" class="mb-2">
      <a-slider v-model:value="props.voice.amplitude" />
    </a-form-item>
    <a-form-item label="Test voice" :labelCol="{ span: 3 }" class="mb-2">
      <a-input-search :placeholder="defaultTest" v-model:value="test" @search="testVoice">
        <template #enterButton>
          <sound-outlined />
        </template>
      </a-input-search>
    </a-form-item>
  </template>
</template>