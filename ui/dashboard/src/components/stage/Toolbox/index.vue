<template>
  <TopBar :tool="tool" />
  <nav id="toolbox" :class="{ collapsed }" class="panel">
    <div class="panel-body">
      <PanelItem name="Backdrop" icon="backdrop.svg" />
      <PanelItem name="Avatars" icon="avatar.svg" />
      <PanelItem name="Props" icon="prop.svg" />
      <PanelItem name="Audio" icon="audio.svg" />
      <PanelItem name="Stream" icon="stream.svg" />
      <PanelItem name="Draw" icon="draw.svg" />
      <PanelItem name="Text" icon="text.svg" />
      <PanelItem name="Setting" icon="rotation-slider.svg" />
      <PanelItem name="Curtain" icon="curtain.svg" />
      <PanelItem name="Depth" icon="multi-frame.svg" />
      <PlayerChat />
      <a class="panel-block stage-scene-toggle" @click="changeTool('Scene')">
        <span>
          <Icon v-if="isScene" size="36" src="stage.svg" />
          <Icon v-else size="36" src="scene.svg" />
        </span>
      </a>
    </div>
  </nav>
</template>

<script>
import { computed, provide, ref } from "vue";
import TopBar from "./TopBar";
import PanelItem from "./PanelItem";
import PlayerChat from "./PlayerChat";
import Icon from "@/components/Icon";

export default {
  components: { TopBar, PanelItem, PlayerChat, Icon },
  setup: () => {
    const tool = ref();
    const changeTool = (newTool) => {
      if (tool.value === newTool) {
        tool.value = undefined;
      } else {
        tool.value = newTool;
      }
    };
    provide("tool", tool);
    provide("changeTool", changeTool);

    const collapsed = ref(true);
    const timer = ref();
    const expand = () => {
      collapsed.value = false;
      clearTimeout(timer.value);
    };
    const waitToCollapse = () => {
      timer.value = setTimeout(() => (collapsed.value = true), 1000);
    };

    waitToCollapse();

    const isScene = computed(() => tool.value === "Scene");

    return {
      tool,
      changeTool,
      collapsed,
      expand,
      waitToCollapse,
      isScene,
    };
  },
};
</script>

<style lang="scss">
#toolbox {
  position: fixed;
  width: 15%;
  min-width: 200px;
  left: 16px;
  background-color: white;
  opacity: 0.9;
  transition: transform 0.5s;
  top: 120px;
  z-index: 2;

  .panel-icon {
    width: 1.5em;
    filter: grayscale(100%);
  }
  .panel-block.is-active,
  .panel-block:hover {
    border: none;
    .panel-icon {
      filter: none;
      transform: scale(1.5);
    }
  }
  .stage-scene-toggle {
    height: 62px;
    > span {
      position: absolute;
      right: 0px;
      bottom: 8px;
    }
  }

  &.collapsed {
    transform: translateX(-90%);
    .panel-icon {
      position: absolute;
      right: 0;
    }
    .fa-angle-right {
      display: none;
    }
  }

  .dropdown-menu {
    position: fixed;
    left: 216px;
    top: initial;
    z-index: 100;
  }
}
</style>