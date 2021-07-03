<template>
  <div @click="create" class="is-pulled-left">
    <div class="icon is-large">
      <Icon src="new.svg" size="36" />
    </div>
    <span class="tag is-light is-block">Blank Scene</span>
  </div>
  <Scene v-for="scene in scenes" :key="scene.id" :scene="scene" />
  <div v-if="saving">
    <Loading height="64px" />
  </div>
  <div v-else @click="saveScene" class="is-pulled-left">
    <div class="icon is-large">
      <Icon src="save.svg" size="36" />
    </div>
    <span class="tag is-light is-block">Save Scene</span>
  </div>
</template>

<script>
import { useStore } from "vuex";
import Icon from "@/components/Icon";
import Loading from "@/components/Loading";
import html2canvas from "html2canvas";
import { cropImageFromCanvas } from "@/utils/canvas";
import { ref } from "@vue/reactivity";
import { useMutation } from "@/services/graphql/composable";
import { stageGraph } from "@/services/graphql";
import { computed } from "@vue/runtime-core";
import Scene from "./Scene";

export default {
  components: { Icon, Loading, Scene },
  setup: () => {
    const store = useStore();
    const newScene = () => {
      console.log(store);
    };

    const saving = ref(false);
    const saveScene = async () => {
      try {
        saving.value = true;
        const el = document.querySelector("#board");
        const { width } = el.getBoundingClientRect();
        const canvas = await html2canvas(el, { scale: 200 / width });
        const preview = cropImageFromCanvas(canvas)?.src;
        const stageId = store.state.stage.model.dbId;
        const {
          background,
          curtain,
          backdropColor,
          board,
          settings,
          tools,
          audioPlayers,
        } = store.state.stage;
        const payload = JSON.stringify({
          background,
          curtain,
          backdropColor,
          board,
          settings,
          tools,
          audioPlayers,
        });

        const { save } = useMutation(stageGraph.saveScene);
        await save("Scene saved successfully!", { stageId, payload, preview });
        store.dispatch("stage/loadScenes");
      } catch (error) {
        console.log(error);
      } finally {
        saving.value = false;
      }
    };

    const scenes = computed(() => store.state.stage.model.scenes);

    return { newScene, saveScene, saving, scenes };
  },
};
</script>

<style lang="scss" scoped>
@import "@/styles/mixins.scss";
.fas.fa-plus {
  @include gradientText(#30ac45, #6fb1fc);
}
video {
  height: 100%;
}
</style>