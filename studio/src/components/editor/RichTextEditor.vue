<template>
  <Space direction="vertical" class="w-full shadow rounded-xl bg-white">
    <Editor :key="readonly ? 'readonly' : 'default'" :init="{
      height: 500,
      menubar: false,
      plugins: [
        'advlist autolink lists link image charmap print preview anchor',
        'searchreplace visualblocks code fullscreen',
        'insertdatetime media table paste code help wordcount',
        'image',
        'table',
      ],
      toolbar: readonly ? '' :
        'undo redo | formatselect | bold italic backcolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat | link | table | image | code | help',
    }" v-bind="$attrs" />
  </Space>
</template>

<script setup>
import Editor from "@tinymce/tinymce-vue";
import { Space } from "ant-design-vue";
import { defineProps, ref, watch } from 'vue'
const props = defineProps({
  readonly: Boolean
})
const readonly = ref(props.readonly);
watch(() => props.readonly, (newVal, oldVal) => {
  readonly.value = newVal
})
</script>
