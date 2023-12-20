<template>
  <div v-if="!modelValue" class="card-header">
    <span class="card-header-title">{{ $t("voice_setting") }}</span>
  </div>
  <div class="card-content voice-parameters">
    <HorizontalField title="Voice">
      <Dropdown
        v-model="parameters.voice"
        :data="voices"
        :render-label="(voice) => voice.name"
        :render-value="(voice) => voice.id"
        style="width: 100%"
        fixed
      />
    </HorizontalField>

    <template v-if="parameters.voice">
      <HorizontalField title="Variant">
        <Dropdown
          v-model="parameters.variant"
          :data="variants"
          :render-label="(variant) => variant.name"
          :render-value="(variant) => variant.id"
          style="width: 100%"
          fixed
        />
      </HorizontalField>

      <HorizontalField title="Pitch">
        <input
          class="slider is-fullwidth is-primary m-0"
          v-model="parameters.pitch"
          type="range"
          min="0"
          max="100"
          step="1"
        />
      </HorizontalField>
      <HorizontalField title="Rate">
        <input
          class="slider is-fullwidth is-primary m-0"
          v-model="parameters.speed"
          type="range"
          min="0"
          max="350"
          step="1"
        />
      </HorizontalField>

      <HorizontalField title="Volume">
        <input
          class="slider is-fullwidth is-primary m-0"
          v-model="parameters.amplitude"
          type="range"
          min="0"
          max="100"
          step="1"
        />
      </HorizontalField>

      <HorizontalField title="Test voice">
        <InputButtonPostfix v-model="test" @ok="testVoice">
          <template #icon>
            <span class="icon">
              <Icon src="voice-setting-invert.svg" />
            </span>
          </template>
        </InputButtonPostfix>
      </HorizontalField>
    </template>
    <SaveButton v-if="!modelValue" @click="save" />
  </div>
</template>

<script>
import { computed, reactive, ref } from "vue";
import SaveButton from "@/components/form/SaveButton";
import Dropdown from "@/components/form/Dropdown";
import HorizontalField from "@/components/form/HorizontalField";
import InputButtonPostfix from "@/components/form/InputButtonPostfix";
import Icon from "@/components/Icon";
import { useStore } from "vuex";
import { avatarSpeak } from "@/services/speech";
import {
  getDefaultVariant,
  getVariantList,
  getVoiceList,
} from "@/services/speech/voice";

export default {
  components: {
    SaveButton,
    Dropdown,
    HorizontalField,
    InputButtonPostfix,
    Icon,
  },
  props: ["modelValue"],
  emits: ["close", "update:modelValue"],
  setup: (props, { emit }) => {
    const store = useStore();
    const currentAvatar = computed(() => store.getters["stage/currentAvatar"]);
    const voices = [{ id: undefined, name: 'No voice' }].concat(getVoiceList());
    const variants = getVariantList();
    const parameters = reactive(
      props.modelValue ? props.modelValue : currentAvatar.value?.voice
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
  .dropdown-trigger > button,
  .dropdown-menu {
    width: 100%;
  }
}
</style>