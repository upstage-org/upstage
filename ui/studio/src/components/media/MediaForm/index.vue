<script setup lang="ts">
import { useQuery } from '@vue/apollo-composable';
import { Modal } from 'ant-design-vue';
import { ExclamationCircleOutlined } from '@ant-design/icons-vue';
import gql from 'graphql-tag';
import { ref, computed, inject, Ref, createVNode, watch } from 'vue'
import { SlickList, SlickItem } from 'vue-slicksort';
import { CopyrightLevel, Media, MediaAttributes, StudioGraph, UploadFile } from '../../../models/studio';
import { absolutePath, capitalize } from '../../../utils/common';
import StageAssignment from './StageAssignment.vue';
import { useSaveMedia } from './composable';
import { editingMediaVar, inquiryVar } from '../../../apollo';
import MediaPermissions from './MediaPermissions.vue';
const files = inject<Ref<UploadFile[]>>("files")

const { result: editingMediaResult } = useQuery<{ editingMedia: Media }>(gql`{ editingMedia @client }`);

watch(editingMediaResult, () => {
  if (editingMediaResult.value) {
    const { editingMedia } = editingMediaResult.value;
    name.value = editingMedia.name;
    type.value = editingMedia.assetType.name;
    tags.value = editingMedia.tags;
    copyrightLevel.value = editingMedia.copyrightLevel;
    const attributes = JSON.parse(editingMedia.description) as MediaAttributes;
    if (files?.value) {
      const frames = attributes.frames && attributes.frames.length ? attributes.frames : [editingMedia.src];
      files.value = frames.map((frame, id) => ({
        id,
        preview: absolutePath(frame),
        url: frame,
        status: 'uploaded',
        file: {
          name: editingMedia.name,
        } as File
      }));
    }
    if (editingMedia.stages) {
      stageIds.value = editingMedia.stages.map(stage => stage.id);
    }
    userIds.value = editingMedia.permissions.filter(permission => permission.approved).map(permission => permission.userId);
  }
});

const name = ref('')
const type = ref('avatar')
const tags = ref<string[]>([])
const stageIds = ref<number[]>([])
const userIds = ref<number[]>([])
const mediaName = computed(() => {
  if (name.value) {
    return name.value
  }
  if (files && files.value.length) {
    return files.value[0].file.name
  }
  return ''
})
const copyrightLevel = ref<CopyrightLevel>(0)

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
    if (editingMediaResult.value) {
      editingMediaVar(undefined)
      files.value = []
    } else {
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
  tags {
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
      id: editingMediaResult.value?.editingMedia?.id,
      name: mediaName.value,
      mediaType: type.value,
      copyrightLevel: copyrightLevel.value,
      stageIds: stageIds.value,
      userIds: userIds.value,
      tags: tags.value,
      w: frameSize.value.width,
      h: frameSize.value.height,
      urls: [],
    }
  }
}, id => {
  if (files && refresh) {
    files.value = []
    refresh()
  }
})

watch(files as Ref, ([firstFile]) => {
  if (firstFile && firstFile.status === 'local' && firstFile.file.type.includes('audio')) {
    type.value = 'audio'
  } else if (firstFile && firstFile.status === 'local' && firstFile.file.type.includes('video')) {
    type.value = 'stream'
  } else if (firstFile && firstFile.status === 'local' && (!type.value || type.value === 'stream' || type.value === 'audio')) {
    type.value = 'avatar'
  }
})

const visibleDropzone = inject('visibleDropzone')
const composingMode = inject<Ref<boolean>>('composingMode')

const addExistingFrame = () => {
  if (composingMode) {
    composingMode.value = true
    inquiryVar({
      ...inquiryVar(),
      mediaTypes: [type.value]
    })
  }
}

const frameSize = ref({ width: 100, height: 100 })
const handleImageLoad = (e: Event, index: number) => {
  if (index === 0 && e.target) {
    const { width, height } = e.target as HTMLImageElement
    if (width > height) {
      frameSize.value = {
        width: 100,
        height: (100 * height) / width
      }
    } else {
      frameSize.value = {
        width: (100 * width) / height,
        height: 100
      }
    }
  }
}
</script>

<template>
  <a-modal
    :visible="files?.length && !composingMode"
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
        <a-button type="primary" @click="addExistingFrame">
          <PlusCircleOutlined />Add existing frame
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
        <div class="bg-gray-200 flex items-center justify-center h-full max-h-96">
          <audio v-if="type === 'audio'" controls class="w-48">
            <source v-if="files && files.length" :src="files[0].preview" />Your browser does not support the audio element.
          </audio>
          <video v-else-if="type === 'stream'" controls class="w-48">
            <source v-if="files && files.length" :src="files[0].preview" />Your browser does not support the video tag.
          </video>
          <SlickList
            v-else
            axis="y"
            v-model:list="files"
            class="cursor-move w-full max-h-96 overflow-auto"
            :class="{ 'cursor-not-allowed': clearMode }"
            @sort-start="handleFrameClick"
          >
            <SlickItem v-for="(file, i) in files" :key="file.id" :index="i" style="z-index: 99999;">
              <div class="my-2 px-8 text-center">
                <img
                  show-handle
                  :src="file.preview"
                  class="max-w-full rounded-md max-h-24"
                  @load="handleImageLoad($event, i)"
                />
              </div>
            </SlickItem>
          </SlickList>
        </div>
        <a-alert
          v-if="files!.length > 1"
          :message="clearMode ? 'Click a frame to remove it' : 'Drag a frame to reorder its position'"
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
            <a-tab-pane key="permissions" tab="Permissions">
              <MediaPermissions
                :key="editingMediaResult?.editingMedia?.id"
                v-model="copyrightLevel"
                v-model:users="userIds"
                :media="editingMediaResult?.editingMedia"
              />
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
      <a-space>
        <a-select
          class="text-left"
          style="min-width: 200px;"
          v-model:value="tags"
          mode="tags"
          placeholder="Tags"
          :options="result ? result.tags.edges.map(({ node }) => ({ value: node.name, label: node.name })) : []"
        ></a-select>
        <a-button key="submit" type="primary" :loading="saving" @click="saveMedia">
          <span v-if="saving">Saving {{ progress }}%</span>
          <span v-else>Save</span>
        </a-button>
      </a-space>
    </template>
  </a-modal>
</template>

<style>
:deept(.ant-progress-outer) {
  padding-right: 0;
}
</style>