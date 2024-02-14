<template>
  <BlankScene />
  <Scene v-for="scene in scenes" :key="scene.id" :scene="scene" />
  <div v-if="saving">
    <Loading height="64px" />
  </div>
  <div v-else @click="saveScene" class="is-pulled-left">
    <div class="icon is-large">
      <Icon src="save.svg" size="36" />
    </div>
    <span class="tag is-light is-block">{{ $t("save_scene") }}</span>
  </div>
</template>

<script>
import { useStore } from "vuex";
import Icon from "@/components/Icon";
import Loading from "@/components/Loading";
import { computed } from "vue";
import Scene from "./Scene";
import BlankScene from "./BlankScene";

export default {
  components: { Icon, Loading, BlankScene, Scene },
  setup: () => {
    const store = useStore();

    const saving = computed(() => store.state.stage.isSavingScene);

    const scenes = computed(() => store.state.stage.model.scenes);
    const saveScene = () => {
      store.dispatch("stage/openSettingPopup", {
        type: "SaveScene",
      });
    };

    return { saving, scenes, saveScene };
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
