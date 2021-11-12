<script setup lang="ts">
import { useQuery } from '@vue/apollo-composable';
import { Modal } from 'ant-design-vue';
import { ExclamationCircleOutlined } from '@ant-design/icons-vue';
import gql from 'graphql-tag';
import { ref, computed, inject, Ref, createVNode } from 'vue'
import { SlickList, SlickItem } from 'vue-slicksort';
import { StudioGraph } from '../../../models/studio';
import { capitalize } from '../../../utils/common';
import StageAssignment from './StageAssignment.vue';
import { useSaveMedia } from './composable';
const files: Ref<any[]> | undefined = inject("files")

const name = ref('')
const type = ref('avatar')
const stageIds = ref([])
const mediaName = computed(() => {
  if (name.value) {
    return name.value
  }
  if (files && files.value.length) {
    return files.value[0].file.name
  }
})

const handleFrameClick = ({ event, index }: { event: any, index: number }) => {
  console.log(event)
  event.preventDefault()
  if (!clearMode.value) {
    return
  }
  if (files && files.value.length > 1) {
    const filesCopy = files.value.slice()
    Modal.confirm({
      title: 'Are you sure you want to remove this frame?',
      icon: createVNode(ExclamationCircleOutlined),
      content: createVNode('div', { style: 'color: orange;' }, 'There is no undo!'),
      onOk() {
        files.value = filesCopy.filter((_, i) => i !== index)
        if (files.value.length === 1) {
          clearMode.value = false
        }
      },
      okButtonProps: {
        danger: true
      }
    });
  }
}

const handleClose = () => {
  if (files) {
    if (files.value.length) {
      Modal.confirm({
        title: 'Are you sure you want to quit?',
        icon: createVNode(ExclamationCircleOutlined),
        content: createVNode('div', { style: 'color: orange;' }, 'All selected frames will be lost, there is no undo!'),
        onOk() {
          files.value = []
        },
        okButtonProps: {
          danger: true
        }
      });
    } else {
      files.value = []
    }
  }
}

const clearMode = ref(false)

const { result, loading } = useQuery<StudioGraph>(gql`
{
  mediaTypes {
    edges {
      node {
        name
      }
    }
  }
}
`, null, { fetchPolicy: "cache-only" })
const mediaTypes = computed(() => {
  if (result.value?.mediaTypes) {
    return result.value.mediaTypes.edges.map(({ node }) => ({ label: capitalize(node.name), value: node.name }))
  }
  return []
})

const refresh = inject("refresh") as () => any
const { progress, saveMedia, saving } = useSaveMedia(() => {
  return {
    files: files ? files.value : [],
    media: {
      name: mediaName.value,
      mediaType: type.value,
      copyrightLevel: 0,
      stageIds: stageIds.value
    }
  }
}, id => {
  if (files && refresh) {
    files.value = []
    refresh()
  }
})

const visibleDropzone = inject('visibleDropzone')
</script>

<template>
  <a-modal
    :visible="files?.length"
    :body-style="{ padding: 0 }"
    :width="1000"
    @cancel="handleClose"
  >
    <template #title>
      <a-space>
        <a-input-group compact>
          <a-select :options="mediaTypes" v-model:value="type"></a-select>
          <a-input v-model:value="name" :placeholder="mediaName"></a-input>
        </a-input-group>
        <a-button type="primary" @click="visibleDropzone = true">
          <UploadOutlined />Upload frame
        </a-button>
        <a-button type="primary">
          <PlusCircleOutlined />Add existed frame
        </a-button>
        <a-button
          v-if="files!.length > 1"
          :type="clearMode ? 'primary' : 'dashed'"
          danger
          @click="clearMode = !clearMode"
        >
          <ClearOutlined />Clear frames
        </a-button>
      </a-space>
    </template>
    <a-row :gutter="12">
      <a-col :span="6">
        <div class="bg-gray-200 flex items-center h-full max-h-96">
          <SlickList
            axis="y"
            v-model:list="files"
            class="cursor-move w-full max-h-96 overflow-auto"
            :class="{ 'cursor-not-allowed': clearMode }"
            @sort-start="handleFrameClick"
          >
            <SlickItem v-for="(file, i) in files" :key="file.id" :index="i" style="z-index: 99999;">
              <div class="my-2 px-8 text-center">
                <img show-handle :src="file.preview" class="max-w-full rounded-md max-h-24" />
              </div>
            </SlickItem>
          </SlickList>
        </div>
        <a-alert
          v-if="files!.length > 1"
          :message="clearMode ? 'Click a frame to remove it' : 'Drag a frame to reorder it\'s position'"
          :type="clearMode ? 'error' : 'success'"
          show-icon
          closable
          class="text-sm"
        />
      </a-col>
      <a-col :span="18">
        <div class="card-container pr-4">
          <a-tabs>
            <a-tab-pane key="stages" tab="Stages" class="pb-4">
              <StageAssignment v-model="stageIds" />
            </a-tab-pane>
            <a-tab-pane key="c" tab="Copyrights">
              <a-result title="UNDER CONSTRUCTION" sub-title="Please come back later!">
                <template #icon>
                  <BuildOutlined />
                </template>
              </a-result>
            </a-tab-pane>
            <a-tab-pane key="voice" tab="Voice">
              <a-result title="UNDER CONSTRUCTION" sub-title="Please come back later!">
                <template #icon>
                  <BuildOutlined />
                </template>
              </a-result>
            </a-tab-pane>
          </a-tabs>
        </div>
      </a-col>
    </a-row>
    <a-progress
      v-if="saving"
      :stroke-color="{
        from: '#108ee9',
        to: '#87d068',
      }"
      :percent="progress"
      status="active"
      class="absolute left-0 bottom-10"
      :show-info="false"
    >
      <template #format></template>
    </a-progress>
    <template #footer>
      <a-button key="submit" type="primary" :loading="saving" @click="saveMedia">
        <span v-if="saving">Saving {{ progress }}%</span>
        <span v-else>Save</span>
      </a-button>
    </template>
  </a-modal>
</template>

<style>
:deept(.ant-progress-outer) {
  padding-right: 0;
}
</style>