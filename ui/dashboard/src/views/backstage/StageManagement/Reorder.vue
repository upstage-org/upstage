<template>
  <div v-for="mediaType in types" :key="mediaType" class="columns is-vcentered has-text-centered">
    <div class="column is-1">
      <h4 class="subtitle">
        <Icon :src="mediaType + '.svg'" />
        <br />
        {{ mediaType }}
        <br />
        <small>({{ mediaGroups[mediaType].length }})</small>
      </h4>
    </div>
    <div class="column is-11">
      <div class="toolbox">
        <div class="scroller">
          <div
            v-for="item in mediaGroups[mediaType]"
            :key="item.id"
            :id="item.id"
            class="media-preview"
            draggable="true"
            @dragstart="dragstart"
            @dragend="dragend"
            @dragenter.prevent
            @dragover.prevent="dragover"
            @dragleave.prevent="dragleave"
            @drop.prevent="drop"
          >
            <div style="pointer-events: none;">
              <div v-if="mediaType === 'audio'">
                <Icon src="audio.svg" />
                <br />
                <b>{{ item.name }}</b>
              </div>
              <div v-else-if="mediaType === 'stream'">
                <Icon src="stream.svg" />
                <br />
                <b>{{ item.name }}</b>
              </div>
              <Asset v-else :asset="item" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, computed } from 'vue';
import Icon from "@/components/Icon.vue";
import Asset from "@/components/Asset.vue";

const props = defineProps({
  modelValue: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits(['update:modelValue'])

const types = computed(() => [...new Set(props.modelValue.map(media => media.mediaType))])
const mediaGroups = computed(() => {
  const res = {}
  props.modelValue.forEach((item) => {
    res[item.mediaType] = (res[item.mediaType] ?? []).concat(item)
  });
  return res;
})

const dragstart = (e) => {
  e.target.classList.add('dragging');
  e.dataTransfer.setDragImage(e.target, 0, 0);
  e.dataTransfer.setData('text/plain', e.target.id);
}

const dragend = (e) => {
  e.target.classList.remove('dragging');
}

const dragover = (e) => {
  e.target.classList.add('dropzone')
}

const dragleave = (e) => {
  e.target.classList.remove('dropzone')
}

const drop = (e) => {
  e.target.classList.remove('dropzone')
  const fromId = e.dataTransfer.getData('text/plain')
  const toId = e.target.id
  const fromIndex = props.modelValue.findIndex(t => t.id === fromId)
  const toIndex = props.modelValue.findIndex(t => t.id === toId)
  if (fromIndex > -1 && toIndex > -1) {
    const media = props.modelValue.splice(fromIndex, 1)[0]
    emit('update:modelValue', props.modelValue.slice(0, toIndex).concat(media).concat(props.modelValue.slice(toIndex)))
  }
}
</script>

<style scoped lang="scss">
@import "@/styles/bulma";

.subtitle {
  text-transform: capitalize;
  margin-bottom: 0;
}
.toolbox {
  background-color: #fdedf6;
  border-radius: 8px;
  width: 100%;
  max-width: max-content;
  overflow-x: auto;
  margin-bottom: 6px;
  .scroller {
    width: max-content;
    cursor: grab;
  }
  .media-preview {
    float: left;
    width: 100px;
    height: 100px;
    padding: 8px;
    overflow: hidden;

    > div {
      width: 100%;
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      transition-duration: 0.25s;
    }
    &:hover {
      img {
        -webkit-filter: drop-shadow(0 0 4px $dark);
        filter: drop-shadow(0 0 4px $dark);
      }
    }
  }
  .dropzone {
    background: repeating-radial-gradient(
      circle,
      green,
      green 10px,
      #007011 10px,
      #007011 20px
    );
    > * {
      transform: translateX(50%) !important;
    }
  }
  .dragging {
    opacity: 0.5;
  }
}
</style>
