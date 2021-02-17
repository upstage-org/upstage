<template>
  <TopBar :tool="tool" />
  <nav
    id="toolbox"
    :class="{ collapsed }"
    class="panel"
    @mouseenter="expand"
    @mouseleave="waitToCollapse"
  >
    <div class="panel-heading p-0 m-0 tabs is-toggle is-fullwidth">
      <ul>
        <li class="is-active">
          <a>
            <span>Stage</span>
          </a>
        </li>
        <li>
          <a class="button">
            <span>Scene</span>
          </a>
        </li>
      </ul>
    </div>
    <div class="panel-body">
      <a
        @click="changeTool('Backdrop')"
        :class="{ 'is-active': tool === 'Backdrop' }"
        class="panel-block button"
      >
        <span class="panel-icon">
          <Icon src="backdrop.svg" />
        </span>
        Backdrop
      </a>
      <a
        @click="changeTool('Avatars')"
        :class="{ 'is-active': tool === 'Avatars' }"
        class="panel-block button"
      >
        <span class="panel-icon">
          <Icon src="avatar.svg" />
        </span>
        Avatars
      </a>
      <a
        @click="changeTool('Props')"
        :class="{ 'is-active': tool === 'Props' }"
        class="panel-block button"
      >
        <span class="panel-icon">
          <Icon src="props.svg" />
        </span>
        Props
      </a>
      <a
        @click="changeTool('Audio')"
        :class="{ 'is-active': tool === 'Audio' }"
        class="panel-block button"
      >
        <span class="panel-icon">
          <Icon src="audio.svg" />
        </span>
        Audio
      </a>
      <div class="dropdown is-hoverable is-fullwidth">
        <div class="dropdown-trigger is-fullwidth">
          <a
            @click="changeTool('Stream')"
            :class="{ 'is-active': tool === 'Stream' }"
            class="panel-block button"
          >
            <span class="panel-icon">
              <Icon src="stream.svg" />
            </span>
            <span class="is-fullwidth">Streams</span>
            <span class="icon is-small">
              <i class="fas fa-angle-right" aria-hidden="true"></i>
            </span>
          </a>
          <span />
        </div>
        <div class="dropdown-menu" id="dropdown-menu4" role="menu">
          <div class="dropdown-content">
            <a href="#" class="dropdown-item button" @click="createStream()">
              Add New
            </a>
            <a
              href="#"
              class="dropdown-item button"
              @click="changeTool('Stream')"
            >
              Manage
            </a>
          </div>
        </div>
      </div>
      <div class="dropdown is-hoverable is-fullwidth">
        <div class="dropdown-trigger is-fullwidth">
          <a
            @click="changeTool('Draw')"
            :class="{ 'is-active': tool === 'Draw' }"
            class="panel-block button"
          >
            <span class="panel-icon">
              <Icon src="draw.svg" />
            </span>
            <span class="is-fullwidth">Draw</span>
            <span class="icon is-small">
              <i class="fas fa-angle-right" aria-hidden="true"></i>
            </span>
          </a>
          <span />
        </div>
        <div class="dropdown-menu" id="dropdown-menu4" role="menu">
          <div class="dropdown-content">
            <a
              href="#"
              class="dropdown-item button"
              @click="openDrawTool(true)"
            >
              Add New
            </a>
            <a
              href="#"
              class="dropdown-item button"
              @click="openDrawTool(false)"
            >
              Manage
            </a>
          </div>
        </div>
      </div>
      <a
        @click="createText"
        :class="{ 'is-active': tool === 'Text' }"
        class="panel-block button"
      >
        <span class="panel-icon">
          <Icon src="text.svg" />
        </span>
        Text
      </a>
    </div>
    <div class="panel-block">
      <button class="button is-fullwidth is-block">
        <span class="icon">
          <Icon src="savescene.svg" />
        </span>
        <span>Save Scene</span>
      </button>
    </div>
  </nav>
</template>

<script>
import { ref } from "vue";
import TopBar from "./TopBar";
import { useStore } from "vuex";
import Icon from "@/components/Icon";

export default {
  components: { TopBar, Icon },
  setup: () => {
    const tool = ref();
    const changeTool = (newTool) => {
      if (tool.value === newTool) {
        tool.value = undefined;
      } else {
        tool.value = newTool;
      }
    };
    const collapsed = ref(false);
    const timer = ref();
    const expand = () => {
      collapsed.value = false;
      clearTimeout(timer.value);
    };
    const waitToCollapse = () => {
      timer.value = setTimeout(() => (collapsed.value = true), 1000);
    };

    waitToCollapse();

    const store = useStore();
    const openDrawTool = (isDrawing) => {
      tool.value = "Draw";
      store.commit("stage/UPDATE_IS_DRAWING", isDrawing);
    };

    const createStream = () => {
      changeTool("Stream");
      store.dispatch("stage/openSettingPopup", {
        type: "CreateStream",
      });
    };

    const createText = () => {
      changeTool("Text");
      store.dispatch("stage/openSettingPopup", {
        type: "CreateText",
      });
    };

    return {
      tool,
      changeTool,
      collapsed,
      expand,
      waitToCollapse,
      openDrawTool,
      createStream,
      createText,
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
  }

  &.collapsed {
    transform: translateX(-85%);
    .panel-icon {
      position: relative;
      left: 150px;
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

  .panel-block button.is-active {
    border-left-width: 2px;
    border-left-style: solid;
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