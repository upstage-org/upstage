<template>
  <Editor
    :init="{
      height: 500,
      menubar: false,
      plugins: [
        'advlist autolink lists link image charmap print preview anchor',
        'searchreplace visualblocks code fullscreen',
        'insertdatetime media table paste code help wordcount',
        'image',
        'table'
      ],
      toolbar:
        'undo redo | formatselect | bold italic backcolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat | link | table | image | code | help'
    }"
    v-bind="$attrs"
  />
</template>

<script setup>
import Editor from '@tinymce/tinymce-vue';
</script>