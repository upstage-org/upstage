<script setup lang="ts">
import { Layout } from "ant-design-vue";
import RichTextEditor from "components/editor/RichTextEditor.vue";
import { ref } from "vue";

const content = ref(
  `<h1>Notification Title</h1><p>Dear UpStage Users,</p><p>Thank you and best regards,</p><p><img src="	https://upstage.live/img/upstage.00bba63e.png" alt="@upstage-org">`
);
</script>

<template>
  <Layout class="bg-white rounded-lg">
    <a-form-item
      :label="$t('body')"
      :label-col="{ span: 12, xl: { span: 4 }, xxl: { span: 3 } }"
    >
      <RichTextEditor v-model="content" />
    </a-form-item>
  </Layout>
</template>
