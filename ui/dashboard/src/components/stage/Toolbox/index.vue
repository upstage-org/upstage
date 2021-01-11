<template>
  <TopBar :tool="tool" />
  <nav id="toolbox" class="panel">
    <div class="panel-heading p-0 m-0 tabs is-toggle is-fullwidth">
      <ul>
        <li class="is-active">
          <a>
            <span>Stage</span>
          </a>
        </li>
        <li>
          <a>
            <span>Scene</span>
          </a>
        </li>
      </ul>
    </div>
    <div class="panel-body">
      <a
        @click="changeTool('Avatars')"
        :class="{ 'is-active': tool === 'Avatars' }"
        class="panel-block"
      >
        <span class="panel-icon">
          <i class="fas fa-folder" aria-hidden="true"></i>
        </span>
        Avatars
      </a>
      <a
        @click="changeTool('Props')"
        :class="{ 'is-active': tool === 'Props' }"
        class="panel-block"
      >
        <span class="panel-icon">
          <i class="fas fa-folder" aria-hidden="true"></i>
        </span>
        Props
      </a>
      <a
        @click="changeTool('Backdrops')"
        :class="{ 'is-active': tool === 'Backdrops' }"
        class="panel-block"
      >
        <span class="panel-icon">
          <i class="fas fa-folder" aria-hidden="true"></i>
        </span>
        Backdrops
      </a>
      <a
        @click="changeTool('Text')"
        :class="{ 'is-active': tool === 'Text' }"
        class="panel-block"
      >
        <span class="panel-icon">
          <i class="fas fa-folder" aria-hidden="true"></i>
        </span>
        Text
      </a>
      <a
        @click="changeTool('Audio')"
        :class="{ 'is-active': tool === 'Audio' }"
        class="panel-block"
      >
        <span class="panel-icon">
          <i class="fas fa-folder" aria-hidden="true"></i>
        </span>
        Audio
      </a>
      <a
        @click="changeTool('Draw')"
        :class="{ 'is-active': tool === 'Draw' }"
        class="panel-block"
      >
        <span class="panel-icon">
          <i class="fas fa-folder" aria-hidden="true"></i>
        </span>
        Draw
      </a>
      <label
        @click="changeTool('Streams')"
        :class="{ 'is-active': tool === 'Streams' }"
        class="panel-block"
      >
        <span class="panel-icon">
          <i class="fas fa-folder" aria-hidden="true"></i>
        </span>
        Streams
      </label>
    </div>
    <div class="panel-block">
      <button class="button is-primary is-fullwidth is-block">
        <span class="icon">
          <i class="fas fa-check"></i>
        </span>
        <span>Save Scene</span>
      </button>
    </div>
  </nav>
</template>

<script>
import { ref } from "vue";
import TopBar from "./TopBar";
export default {
  components: { TopBar },
  setup: () => {
    const tool = ref();
    const changeTool = (newTool) => {
      if (tool.value === newTool) {
        tool.value = undefined;
      } else {
        tool.value = newTool;
      }
    };
    return { tool, changeTool };
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
  .panel-block.is-active {
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