<template>
  <SaveButton
    class="mb-4"
    :loading="saving"
    @click="saveCustomisation"
    :disabled="!selectedRatio.width || !selectedRatio.height"
  />
  <table class="is-fullwidth" cellspacing="5">
    <tr>
      <td>
        <h3 class="title">{{ $t("animations") }}</h3>
      </td>
      <td width="100%">
        <div>
          <HorizontalField title="Speech bubble">
            <Dropdown
              v-model="animations.bubble"
              :data="['fade', 'bounce']"
              :render-label="capitalize"
            />
          </HorizontalField>
          <HorizontalField title="Speed">
            <div class="speed-slider">
              <span class="mr-2">{{ $t("slow") }}</span>
              <input
                class="slider is-fullwidth"
                step="0.01"
                min="0.1"
                max="1"
                :value="1000 / animations.bubbleSpeed"
                @change="animations.bubbleSpeed = 1000 / $event.target.value"
                type="range"
              />
              <span class="ml-2">{{ $t("fast") }}</span>
            </div>
          </HorizontalField>
          <HorizontalField title="Curtain">
            <Dropdown
              v-model="animations.curtain"
              :data="[
                { value: 'drop', label: 'Drops down and lifts up' },
                { value: 'fade', label: 'Fades in and out' },
                {
                  value: 'close',
                  label:
                    'Closes from the sides in and opens from the middle out',
                },
              ]"
              :render-value="(item) => item.value"
              :render-label="(item) => item.label"
            />
          </HorizontalField>
          <HorizontalField title="Speed">
            <div class="speed-slider">
              <span class="mr-2">{{ $t("slow") }}</span>
              <input
                class="slider is-fullwidth"
                step="0.01"
                min="0.1"
                max="1"
                :value="5000 / animations.curtainSpeed"
                @change="animations.curtainSpeed = 5000 / $event.target.value"
                type="range"
              />
              <span class="ml-2">{{ $t("fast") }}</span>
            </div>
          </HorizontalField>
        </div>
      </td>
    </tr>
    <tr>
      <td>
        <h3 class="title">{{ $t("streaming") }}</h3>
      </td>
      <td>
        <div>
          <HorizontalField title="Auto detect">
            <Switch v-model="streaming.autoDetect" label="Auto detect for live streams" />
          </HorizontalField>
        </div>
      </td>
    </tr>
    <tr>
      <td>
        <h3 class="title">
          Stage Ratio
          <span
            v-if="selectedRatio"
          >: {{ selectedRatio.width }}/{{ selectedRatio.height }}</span>
        </h3>
      </td>
      <td>
        <div class="columns">
          <div class="column is-3">
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
          <div class="column is-3">
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
          <div class="column is-3">
            <Selectable
              :selected="selectedRatio.width == 2 && selectedRatio.height == 1"
              @select="
              selectedRatio.width = 2;
              selectedRatio.height = 1;
              "
            >
              <div class="box size-option" style="padding-bottom: 50%">
                <div>2/1</div>
              </div>
            </Selectable>
          </div>
          <div class="column is-3">
            <div
              class="box size-option has-primary-background"
              :style="{
                'padding-bottom': `${(selectedRatio.height * 100) / selectedRatio.width
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
      </td>
    </tr>
  </table>
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
    const refresh = inject("refresh");
    const config = useAttribute(stage, "config", true).value ?? {
      ratio: {
        width: 16,
        height: 9,
      },
      animations: {
        bubble: "fade",
        curtain: "drop",
        bubbleSpeed: 1000,
        curtainSpeed: 5000,
      },
      streaming: {
        autoDetect: false,
      },
    };

    const selectedRatio = reactive(config.ratio);
    const animations = reactive(config.animations);
    const streaming = reactive(config.streaming);

    const { loading: saving, save } = useMutation(stageGraph.saveStageConfig);
    const saveCustomisation = async () => {
      const config = JSON.stringify({
        ratio: selectedRatio,
        animations,
        streaming,
      });
      await save(
        () => {
          notification.success("Customisation saved!");
          refresh(stage.value.id);
        },
        stage.value.id,
        config
      );
    };

    return {
      selectedRatio,
      saving,
      saveCustomisation,
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
  white-space: nowrap;
}
.speed-slider {
  display: flex;
  align-items: center;
}
.title {
  white-space: nowrap;
}
td {
  padding: 8px;
}
</style>