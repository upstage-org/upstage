<template>
  <Confirm
    @confirm="(close) => deleteUser({ item, displayName, close, refresh })"
    :loading="loading"
  >
    <template #trigger>
      <a
        class="button is-light is-small is-danger"
        data-tooltip="Delete player"
      >
        <Icon src="delete.svg" />
      </a>
    </template>
    <div class="has-text-centered">
      Deleting user
      <span class="has-text-danger">
        {{ displayName }}
      </span>
      will also delete all of {{ displayName }}'s stages. All of this user's
      media will belong to you. This cannot be undone!
      <br />
      <strong>Are you sure you want to continue?</strong>
    </div>
  </Confirm>
</template>

<script>
import { useMutation } from "@/services/graphql/composable";
import { userGraph } from "@/services/graphql";
import Confirm from "@/components/Confirm";
import Icon from "@/components/Icon";

export default {
  components: { Confirm, Icon },
  props: ["item", "displayName", "refresh"],
  setup: () => {
    const { save, loading } = useMutation(userGraph.deleteUser);
    const deleteUser = async ({ item, displayName, close, refresh }) => {
      await save(`User ${displayName} deleted successfully!`, item);
      refresh();
      close();
    };
    return { loading, deleteUser };
  },
};
</script>

<style></style>
