<template>
  <div v-if="!modelValue" class="card-header">
    <span class="card-header-title">{{ $t("voice_setting") }}</span>
  </div>
  <div class="card-content voice-parameters">
    <a-form-item label="Voice" :labelCol="{ span: 4 }" class="mb-2">
      <a-select v-model:value="parameters.voice" placeholder="No voice" :options="voices" />
    </a-form-item>

    <template v-if="parameters.voice">
      <a-form-item label="Variant" :labelCol="{ span: 4 }" class="mb-2">
        <a-select v-model:value="parameters.variant" :options="variants" />
      </a-form-item>

      <a-form-item label="Pitch" :labelCol="{ span: 4 }" class="mb-2">
        <a-slider v-model:value="parameters.pitch" />
      </a-form-item>

      <a-form-item label="Rate" :labelCol="{ span: 4 }" class="mb-2">
        <a-slider v-model:value="parameters.speed" />
      </a-form-item>
      <a-form-item label="Volume" :labelCol="{ span: 4 }" class="mb-2">
        <a-slider v-model:value="parameters.amplitude" />
      </a-form-item>

      <a-form-item label="Test voice" :labelCol="{ span: 4 }" class="mb-2">
        <a-input-search :placeholder="defaultTestMessage" v-model:value="test" @search="testVoice">
          <template #enterButton>
            <sound-outlined />
          </template>
        </a-input-search>
      </a-form-item>

    </template>
    <SaveButton v-if="!modelValue" @click="save" />
  </div>
</template>

<script>
import { computed, reactive, ref } from "vue";
import SaveButton from "components/form/SaveButton.vue";
import { useStore } from "vuex";
import { avatarSpeak } from "services/speech";
import {
  getDefaultVariant,
  getVariantList,
  getVoiceList,
} from "services/speech/voice";

export default {
  components: {
    SaveButton,
  },
  props: ["modelValue"],
  emits: ["close", "update:modelValue"],
  setup: (props, { emit }) => {
    const store = useStore();
    const currentAvatar = computed(() => store.getters["stage/currentAvatar"]);
    const voices = getVoiceList();
    const variants = getVariantList();
    const parameters = reactive(
      props.modelValue ? props.modelValue : currentAvatar.value?.voice,
    );
    if (!parameters.variant) {
      parameters.variant = getDefaultVariant();
    }
    const test = ref("Welcome to UpStage!");
    const testVoice = () => {
      avatarSpeak({ voice: parameters }, test.value);
    };

    const save = () => {
      store
        .dispatch("stage/shapeObject", {
          ...currentAvatar.value,
          voice: parameters,
        })
        .then(() => emit("close"));
    };

    return { save, parameters, voices, variants, test, testVoice };
  },
};
</script>

<style lang="scss">
.card-footer-item {
  cursor: pointer;
}

.voice-parameters {

  .dropdown,
  .dropdown-trigger,
  .dropdown-trigger>button,
  .dropdown-menu {
    width: 100%;
  }
}

.ant-select-dropdown {
  z-index: 5000 !important;
}
</style>
