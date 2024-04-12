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
import Icon from "components/Icon.vue";
import Loading from "components/Loading.vue";
import { computed } from "vue";
import Scene from "./Scene.vue";
import BlankScene from "./BlankScene.vue";

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
@mixin gradientText($from, $to) {
    background: linear-gradient(to top, $from, $to);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.fas.fa-plus {
  @include gradientText(#30ac45, #6fb1fc);
}
video {
  height: 100%;
}
</style>
