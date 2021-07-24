<template>
  <TopBar :tool="tool" />
  <nav id="toolbox" class="panel">
    <div class="panel-body">
      <PanelItem name="Audio" icon="audio.svg" />
      <hr />
      <PanelItem name="Backdrop" icon="backdrop.svg" />
      <PanelItem name="Avatars" icon="avatar.svg" />
      <PanelItem name="Props" icon="prop.svg" />
      <PanelItem name="Stream" icon="stream.svg" />
      <PanelItem name="Draw" icon="draw.svg" />
      <PanelItem name="Text" icon="text.svg" />
      <hr />
      <PanelItem name="Depth" icon="multi-frame.svg" />
      <PanelItem name="Curtain" icon="curtain.svg" />
      <a class="panel-block stage-scene-toggle" @click="changeTool('Scene')">
        <span>
          <Icon v-if="isScene" size="36" src="stage.svg" />
          <Icon v-else size="36" src="scene.svg" />
        </span>
      </a>
      <hr />
      <PanelItem name="Setting" icon="rotation-slider.svg" />
      <PlayerChat />
    </div>
  </nav>
</template>

<script>
import { computed, provide, ref } from "vue";
import TopBar from "./TopBar";
import PanelItem from "./PanelItem";
import PlayerChat from "./PlayerChat";
import Icon from "@/components/Icon";
import { useStore } from "vuex";

export default {
  components: { TopBar, PanelItem, PlayerChat, Icon },
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

  .panel-icon {
    width: 1.5em;
    img {
      filter: grayscale(100%);
    }
  }
  .panel-block.is-active,
  .panel-block:hover {
    border: none;
    .panel-icon {
      img {
        filter: none;
      }
      transform: scale(1.5);
    }
  }
  .stage-scene-toggle {
    padding-top: 8px;
  }
  hr {
    margin: 0;
  }
}
</style>