<template>
  <TopBar :tool="tool" />
  <nav id="toolbox" :class="{ collapsed }" class="panel">
    <div class="panel-body">
      <PanelItem name="Backdrop" icon="backdrop.svg" />
      <PanelItem name="Avatars" icon="avatar.svg" />
      <PanelItem name="Props" icon="props.svg" />
      <PanelItem name="Audio" icon="audio.svg" />
      <PanelItem name="Stream" icon="stream.svg" />
      <PanelItem name="Draw" icon="draw.svg" />
      <PanelItem name="Text" icon="text.svg" />
      <a class="panel-block stage-scene-toggle">
        <span>
          <Switch
            v-model="isStage"
            checked-label="St"
            unchecked-label="Sc"
            className="is-rounded is-success"
          />
        </span>
      </a>
    </div>
  </nav>
</template>

<script>
import { provide, ref } from "vue";
import TopBar from "./TopBar";
import PanelItem from "./PanelItem";
import Switch from "@/components/form/Switch";

export default {
  components: { TopBar, PanelItem, Switch },
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

    const isStage = ref(true);

    return {
      tool,
      changeTool,
      collapsed,
      expand,
      waitToCollapse,
      isStage,
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
  top: 120px;
  max-height: calc(100% - 130px);
  background-color: white;
  opacity: 0.9;
  transition: transform 0.5s;

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
      transform: rotate(90deg);
      position: absolute;
      right: -10px;
      bottom: 16px;
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

  .panel-body {
    max-height: calc(100vh - 230px);
    overflow-y: auto;
  }

  @media screen and (max-height: 500px) {
    height: calc(100% - 130px);

    .panel-body {
      max-height: calc(100% - 96px);
      overflow-y: auto;
    }
  }
}
</style>