<template>
  <Modal>
    <template #trigger>
      <a class="button is-light is-small" data-tooltip="Edit profile">
        <Icon src="edit.svg" class="clickable" />
      </a>
    </template>
    <template #header>{{ displayName }}'s profile</template>
    <template #content>
      <ProfileForm :profile="item" @success="refresh" />
    </template>
  </Modal>
</template>

<script>
import Modal from "@/components/Modal";
import Icon from "@/components/Icon";
import ProfileForm from "@/components/ProfileForm";

export default {
  components: { Modal, Icon, ProfileForm },
  props: ["item", "displayName", "refresh"],
};
</script>

<style>
button[type="submit"] {
  float: right;
}
</style>