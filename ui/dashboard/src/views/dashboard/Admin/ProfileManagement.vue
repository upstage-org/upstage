<template>
  <UserTable action-column="Edit Profile">
    <template #action="{ item, displayName, refresh }">
      <Modal>
        <template #trigger>
          <i class="fas fa-pen clickable"></i>
        </template>
        <template #header>{{ displayName }}'s profile</template>
        <template #content>
          <ProfileForm :profile="item" @success="refresh" />
        </template>
      </Modal>
    </template>
  </UserTable>
</template>

<script>
import UserTable from "./UserTable";
import Modal from "@/components/Modal";
import ProfileForm from "@/components/ProfileForm";

export default {
  components: { UserTable, Modal, ProfileForm },
};
</script>

<style>
button[type="submit"] {
  float: right;
}
</style>