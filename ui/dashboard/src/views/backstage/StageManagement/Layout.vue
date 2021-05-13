<template>
  <SaveButton
    class="mb-4"
    :loading="saving"
    @click="saveLayout"
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
</template>

<script>
import { reactive } from "@vue/reactivity";
import Selectable from "@/components/Selectable";
import SaveButton from "@/components/form/SaveButton";
import { useAttribute, useMutation } from "@/services/graphql/composable";
import { stageGraph } from "@/services/graphql";
import { notification } from "@/utils/notification";
import { inject } from "@vue/runtime-core";

export default {
  components: { Selectable, SaveButton },
  setup: () => {
    const stage = inject("stage");
    const config = useAttribute(stage, "config", true).value ?? {
      ratio: {
        width: 16,
        height: 9,
      },
    };

    const selectedRatio = reactive(config.ratio);

    const { loading: saving, save } = useMutation(stageGraph.saveStageConfig);
    const saveLayout = async () => {
      const config = JSON.stringify({ ratio: selectedRatio });
      await save(
        () => notification.success("Layout saved successfully!"),
        stage.value.id,
        config
      );
    };

    return { selectedRatio, saving, saveLayout };
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