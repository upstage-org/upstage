<template>
  <Modal width="100%" height="100%">
    <template #trigger>
      <a class="button is-light is-small">
        <i class="fas fa-pen has-text-primary" aria-hidden="true"></i>
      </a>
    </template>
    <MediaForm :media="media" @complete="refresh()" />
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
  inject: ["refresh"],
};
</script>

<style>
</style>