<template>
  <Modal width="500px">
    <template #trigger>
      <a
        class="button is-light is-small is-warning"
        data-tooltip="Reset password"
      >
        <i class="fas fa-key clickable" @click="confirming = false"></i>
      </a>
    </template>
    <template #header>Enter new password for {{ displayName }}</template>
    <template #content>
      <p v-if="confirming">
        Are you sure you want to change password of {{ displayName }} to
        <span class="has-text-danger">{{ password }}</span
        >?
      </p>
      <Field v-else v-model="password" left="fas fa-key" />
    </template>
    <template #footer="{ closeModal }">
      <template v-if="confirming">
        <button class="button is-dark" @click="confirming = false">
          <span class="icon">
            <i class="fas fa-times"></i>
          </span>
          <span>{{ $t("no") }}</span>
        </button>
        <SaveButton
          class="is-dark"
          @click="savePassword(item, displayName, closeModal)"
          :loading="loading"
        >
          <span class="icon">
            <i class="fas fa-shield-alt has-text-warning"></i>
          </span>
          <span>{{ $t("yes") }}</span>
        </SaveButton>
      </template>
      <SaveButton v-else :disabled="!password" @click="confirming = true" />
    </template>
  </Modal>
</template>

<script>
import Modal from "@/components/Modal";
import SaveButton from "@/components/form/SaveButton";
import Field from "@/components/form/Field";
import { ref } from "@vue/reactivity";
import { useMutation } from "@/services/graphql/composable";
import { userGraph } from "@/services/graphql";

export default {
  components: { Modal, SaveButton, Field },
  props: ["user", "displayName"],
  setup: (props) => {
    const password = ref("pleasechange");
    const confirming = ref(false);
    const { save, loading } = useMutation(userGraph.updateUser);
    const savePassword = async (user, displayName, closeModal) => {
      user.password = password.value;
      await save(`Successfully reset ${displayName} password!`, user);
      closeModal();
    };
    return { password, confirming, loading, savePassword, item: props.user };
  },
};
</script>

<style></style>
