<template>
  <SaveButton
    class="mb-4"
    :loading="saving"
    @click="saveCustomization"
    :disabled="!selectedRatio.width || !selectedRatio.height"
  />
  <h3 class="title">
    Stage Ratio
    <span v-if="selectedRatio">
      : {{ selectedRatio.width }}/{{ selectedRatio.height }}
    </span>
  </h3>
  <div class="columns">
    <div class="column">
      <Selectable
        :selected="selectedRatio.width == 4 && selectedRatio.height == 3"
        @select="
          selectedRatio.width = 4;
          selectedRatio.height = 3;
        "
      >
        <div class="box size-option" style="padding-bottom: 75%">
          <div>4/3</div>
        </div>
      </Selectable>
    </div>
    <div class="column">
      <Selectable
        :selected="selectedRatio.width == 16 && selectedRatio.height == 9"
        @select="
          selectedRatio.width = 16;
          selectedRatio.height = 9;
        "
      >
        <div class="box size-option" style="padding-bottom: 56.25%">
          <div>16/9</div>
        </div>
      </Selectable>
    </div>
    <div class="column">
      <div
        class="box size-option has-primary-background"
        :style="{
          'padding-bottom': `${
            (selectedRatio.height * 100) / selectedRatio.width
          }%`,
        }"
      >
        <div>
          <div>Custom ratio:</div>
          <div class="custom-ratio">
            <input type="number" v-model="selectedRatio.width" />
            /
            <input type="number" v-model="selectedRatio.height" />
          </div>
        </div>
      </div>
    </div>
  </div>
  <h3 class="title">Animations</h3>
  <div>
    <HorizontalField title="Speech bubble">
      <Dropdown
        v-model="animations.bubble"
        :data="['fade', 'bounce']"
        :render-label="capitalize"
      />
    </HorizontalField>
  </div>
  <h3 class="title">Streaming</h3>
  <div>
    <HorizontalField title="Auto detect">
      <Switch
        v-model="streaming.autoDetect"
        label="Auto detect for live streams"
      />
    </HorizontalField>
  </div>
</template>

<script>
import { reactive } from "@vue/reactivity";
import Selectable from "@/components/Selectable";
import SaveButton from "@/components/form/SaveButton";
import { useAttribute, useMutation } from "@/services/graphql/composable";
import { stageGraph } from "@/services/graphql";
import { notification } from "@/utils/notification";
import { capitalize, inject } from "@vue/runtime-core";
import HorizontalField from "@/components/form/HorizontalField";
import Dropdown from "@/components/form/Dropdown";
import Switch from "@/components/form/Switch";

export default {
  components: { Selectable, SaveButton, HorizontalField, Dropdown, Switch },
  setup: () => {
    const stage = inject("stage");
    const config = useAttribute(stage, "config", true).value ?? {
      ratio: {
        width: 16,
        height: 9,
      },
      animations: {
        bubble: "fade",
      },
      streaming: {
        autoDetect: false,
      },
    };

    const selectedRatio = reactive(config.ratio);
    const animations = reactive(config.animations);
    const streaming = reactive(config.streaming);

    const { loading: saving, save } = useMutation(stageGraph.saveStageConfig);
    const saveCustomization = async () => {
      const config = JSON.stringify({
        ratio: selectedRatio,
        animations,
        streaming,
      });
      await save(
        () => notification.success("Layout saved successfully!"),
        stage.value.id,
        config
      );
    };

    return {
      selectedRatio,
      saving,
      saveCustomization,
      animations,
      capitalize,
      streaming,
    };
  },
};
</script>

<style lang="scss" scoped>
.size-option {
  width: 100%;
  height: 0;
  padding: 0;
  position: relative;

  > div {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
  }
}
.custom-ratio {
  input {
    width: 50px;
    text-align: center;
  }
}
</style>