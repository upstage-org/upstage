<script setup lang="ts">
import { ref, reactive, computed, watch, inject } from 'vue'
const files: any[] | undefined = inject("files")

const toSrc = ({ file }: { file: File }) => {
  return URL.createObjectURL(file)
}

const name = ref('')
const mediaName = computed(() => {
  if (name.value) {
    return name.value
  }
  if (files && files.length) {
    return files[0].file.name
  }
})

const visible = ref(false)
</script>

<template>
  <a-modal :visible="visible">
    <template #title>
      <a-typography-paragraph
        class="pr-8 mb-0"
        editable
        v-model:value="name"
        @change="(e: string) => name = e"
      >{{ mediaName }}</a-typography-paragraph>
    </template>
    <a-row>
      <a-col :span="4" v-for="file in files">
        <a-image :src="toSrc(file)"></a-image>
      </a-col>
    </a-row>
  </a-modal>
</template>