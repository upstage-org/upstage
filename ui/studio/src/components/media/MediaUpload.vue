<script setup lang="ts">
import { message } from 'ant-design-vue';
import { ref, computed, inject, Ref } from 'vue'
import { SlickList, SlickItem } from 'vue-slicksort';
const files: Ref<any[]> | undefined = inject("files")

const name = ref('')
const mediaName = computed(() => {
  if (name.value) {
    return name.value
  }
  if (files && files.value.length) {
    return files.value[0].file.name
  }
})

const remove = () => {
  message.success('Are you sure you want to remove this?')
}
</script>

<template>
  <a-modal :visible="files?.length">
    <template #title>
      <a-typography-paragraph
        class="pr-8 mb-0"
        editable
        v-model:value="name"
        @change="(e: string) => name = e"
      >{{ mediaName }}</a-typography-paragraph>
    </template>
    <a-row :gutter="12">
      <a-col :span="6">
        <SlickList axis="y" v-model:list="files" class="cursor-move">
          <SlickItem v-for="(file, i) in files" :key="file.id" :index="i" style="z-index: 99999;">
            <img
              show-handle
              :src="file.preview"
              class="w-full mb-2 rounded-md"
              @click.right.prevent="remove"
            />
          </SlickItem>
        </SlickList>
      </a-col>
      <a-col :span="18">
        <a-alert
          message="Drag a frame to reorder it's position, right click to remove it!"
          type="success"
          show-icon
          closable
          class="text-sm"
        />
      </a-col>
    </a-row>
  </a-modal>
</template>