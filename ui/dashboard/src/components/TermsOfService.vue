<template>
  <Modal>
    <template #trigger>
      <a>Terms of Service</a>
    </template>
    <template #header>Terms of Service</template>
    <template #content>
      <Skeleton v-if="loading" />
      <div v-else v-html="content"></div>
    </template>
  </Modal>
</template>

<script>
import { ref } from "@vue/reactivity";
import { onMounted } from "@vue/runtime-core";
import Modal from "@/components/Modal";
import Skeleton from "@/components/Skeleton";
import marked from "marked";

export default {
  components: { Modal, Skeleton },
  setup: () => {
    const url =
      "https://raw.githubusercontent.com/upstage-org/documentation/master/README.md";
    const content = ref();
    const loading = ref(true);

    onMounted(async () => {
      const response = await fetch(url);
      const text = await response.text();
      content.value = marked(text);
      loading.value = false;
    });

    return { content, loading };
  },
};
</script>

<style>
.modal-card-title {
  margin-bottom: 0 !important;
}
</style>