<template>
  <Modal>
    <template #trigger>
      <a>{{ $t("tos.terms_of_service") }}</a>
    </template>
    <template #header>{{ $t("tos.terms_of_service") }}</template>
    <template #content>
      <Loading v-if="loading" />
      <div v-else v-html="content"></div>
    </template>
  </Modal>
</template>

<script>
import { ref } from "vue";
import { computed, watch } from "vue";
import Modal from "@/components/Modal";
import Loading from "@/components/Loading";
import { marked } from "marked";
import { useStore } from "vuex";

export default {
  components: { Modal, Loading },
  setup: () => {
    const store = useStore();
    const url = computed(() => store.getters["config/termsOfService"]);
    const content = ref();
    const loading = ref(true);

    watch(
      url,
      async (value) => {
        if (value) {
          const response = await fetch(url.value);
          const text = await response.text();
          content.value = marked(text);
          loading.value = false;
        }
      },
      { immediate: true },
    );

    return { content, loading };
  },
};
</script>

<style>
.modal-card-title {
  margin-bottom: 0 !important;
}
</style>
