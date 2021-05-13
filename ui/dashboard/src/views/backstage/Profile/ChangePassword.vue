<template>
  <div>
    <Password
      horizontal
      label="Old password"
      v-model="form.oldPassword"
      left="fas fa-lock"
      required
    />
    <Password
      horizontal
      label="New password"
      v-model="form.newPassword"
      left="fas fa-lock"
      required
    />
    <Password
      horizontal
      label="Confirm password"
      v-model="form.confirmPassword"
      left="fas fa-lock"
      :error="confirmPasswordError"
    />
    <ActionsField>
      <button
        class="button mr-2 mt-2 is-primary"
        :class="{ 'is-loading': loading }"
        :disabled="
          !form.oldPassword || !form.newPassword || !form.confirmPassword
        "
        @click="changePassword"
      >
        Change Password
      </button>
    </ActionsField>
  </div>
</template>

<script>
import Password from "@/components/form/Password";
import ActionsField from "@/components/form/ActionsField";
import { computed, reactive } from "vue";
import { useMutation } from "@/services/graphql/composable";
import { userGraph } from "@/services/graphql";
import { notification } from "@/utils/notification";
import { useStore } from "vuex";
export default {
  components: { Password, ActionsField },
  setup: () => {
    const store = useStore();
    const form = reactive({ id: store.state.user.user.id });
    const { loading, mutation } = useMutation(userGraph.changePassword, form);

    const confirmPasswordError = computed(() =>
      form.newPassword !== form.confirmPassword
        ? "Confirm password mismatch"
        : false
    );
    const changePassword = async () => {
      if (confirmPasswordError.value) return;
      try {
        await mutation();
        notification.success("Password changed successfully!");
      } catch (error) {
        notification.error(error);
      }
    };

    return { form, changePassword, loading, confirmPasswordError };
  },
};
</script>

<style>
</style>