<template>
  <TopBar :tool="tool" />
  <nav id="toolbox" class="panel">
    <div class="panel-body">
      <PanelItem name="Audio" icon="audio.svg" />
      <hr />
      <PanelItem name="Backdrops" icon="backdrops.svg" />
      <PanelItem name="Avatars" icon="avatar.svg" />
      <PanelItem name="Props" icon="prop.svg" />
      <PanelItem name="Streams" icon="streams.svg" />
      <PanelItem name="Draw" icon="draw.svg" />
      <PanelItem name="Text" icon="text.svg" />
      <hr />
      <PanelItem name="Depth" icon="multi-frame.svg" />
      <PanelItem name="Curtain" icon="curtain.svg" />
      <PanelItem name="Scenes" icon="animation-slider.svg" />
      <hr />
      <PanelItem name="Settings" icon="rotation-slider.svg" />
      <PlayerChat />
    </div>
  </nav>
</template>

<script>
import { computed, provide, ref } from "vue";
import TopBar from "./TopBar";
import PanelItem from "./PanelItem";
import PlayerChat from "./PlayerChat";
import { useStore } from "vuex";

export default {
  components: { TopBar, PanelItem, PlayerChat },
  setup: () => {
    const tool = ref();
    const store = useStore();
    const changeTool = (newTool) => {
      if (tool.value === newTool) {
        tool.value = undefined;
      } else {
        tool.value = newTool;
      }
      store.commit("stage/SET_ACTIVE_MOVABLE", null);
    };
    provide("tool", tool);
    provide("changeTool", changeTool);

    const isScene = computed(() => tool.value === "Scene");

    return {
      tool,
      changeTool,
      isScene,
    };
  },
};
</script>

<style lang="scss" scoped>
#toolbox {
  position: fixed;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  background-color: white;
  opacity: 0.9;
  transition: transform 0.5s;
  z-index: 2;
  hr {
    margin: 0;
  }
  @media only screen and (orientation: portrait) {
    top: 50px !important;
    transform: none !important;
  }
}
</style>