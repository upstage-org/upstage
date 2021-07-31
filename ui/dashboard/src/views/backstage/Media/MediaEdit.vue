<template>
  <Modal>
    <template #trigger>
      <a class="button is-light is-small">
        <Icon src="edit.svg" />
      </a>
    </template>
    <MediaForm :media="media" @complete="refresh()" />
  </Modal>
  <div></div>
</template>

<script>
import Modal from "@/components/Modal";
import Icon from "@/components/Icon";
import MediaForm from "./MediaForm";

export default {
  components: {
    Modal,
    Icon,
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