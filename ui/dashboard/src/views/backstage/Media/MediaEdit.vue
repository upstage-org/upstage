<template>
  <Modal width="100%">
    <template #trigger>
      <a class="button is-light is-small">
        <i class="fas fa-pen has-text-primary" aria-hidden="true"></i>
      </a>
    </template>
    <template #header> Edit {{ media.name }} </template>
    <template #content>
      <MediaForm :media="media" />
    </template>
  </Modal>
  <div></div>
</template>

<script>
import Modal from "@/components/Modal";
import MediaForm from "./MediaForm";

export default {
  components: {
    Modal,
    MediaForm,
  },
  props: {
    media: Object,
  },
};
</script>

<style>
.field-label {
  padding-top: 0 !important;
  white-space: nowrap;
}
</style>