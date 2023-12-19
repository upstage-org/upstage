<script lang="ts" setup>
import { PropType, reactive, ref } from "vue";
import { AvatarVoice } from "models/studio";
import { avatarSpeak } from "services/speech";
import {
  getVoiceList,
  getVariantList,
  defaultTestMessage,
} from "services/speech/voice";
import VoicePicker from "./VoicePicker.vue";

const props = defineProps({
  voice: {
    type: Object as PropType<AvatarVoice>,
    required: true,
  },
});

const test = ref("");
const testVoice = () => {
  avatarSpeak(props.voice, test.value || defaultTestMessage);
};

const handleVoicePicked = (voice: AvatarVoice) => {
  Object.assign(props.voice, voice);
};
</script>

<template>
  <a-form-item label="Voice" :labelCol="{ span: 3 }" class="mb-2">
    <div class="flex">
      <a-select
        v-model:value="props.voice.voice"
        placeholder="No voice"
        :options="getVoiceList()"
      />
      <VoicePicker @change="handleVoicePicked" />
    </div>
  </a-form-item>
  <template v-if="props.voice.voice">
    <a-form-item label="Variant" :labelCol="{ span: 3 }" class="mb-2">
      <a-select
        v-model:value="props.voice.variant"
        :options="getVariantList()"
      />
    </a-form-item>
    <a-form-item label="Pitch" :labelCol="{ span: 3 }" class="mb-2">
      <a-slider v-model:value="props.voice.pitch" />
    </a-form-item>
    <a-form-item label="Rate" :labelCol="{ span: 3 }" class="mb-2">
      <a-slider
        :value="props.voice.speed / 3.5"
        @change="props.voice.speed = Number($event) * 3.5"
      />
    </a-form-item>
    <a-form-item label="Volume" :labelCol="{ span: 3 }" class="mb-2">
      <a-slider v-model:value="props.voice.amplitude" />
    </a-form-item>
    <a-form-item label="Test voice" :labelCol="{ span: 3 }" class="mb-2">
      <a-input-search
        :placeholder="defaultTestMessage"
        v-model:value="test"
        @search="testVoice"
      >
        <template #enterButton>
          <sound-outlined />
        </template>
      </a-input-search>
    </a-form-item>
  </template>
</template>
