<template>
  <UserTable action-column="Upload Limit">
    <template #action="{ item, displayName }">
      <Confirm
        @confirm="(close) => saveUploadLimit(item, close)"
        :loading="loading"
      >
        <template #render="{ confirm }">
          <input
            class="slider is-fullwidth"
            step="1"
            :min="1024 * 1024"
            :max="nginxLimit"
            type="range"
            v-model="item.uploadLimit"
            :data-tooltip="humanFileSize(item.uploadLimit)"
            @change="confirm"
          />
        </template>
        Are you sure you want to change {{ displayName }}'s upload limit to<br />
        <span class="has-text-danger">
          {{ humanFileSize(item.uploadLimit) }}
        </span>
        ?
      </Confirm>
    </template>
  </UserTable>
</template>

<script>
import UserTable from "./UserTable";
import { useMutation } from "@/services/graphql/composable";
import { userGraph } from "@/services/graphql";
import { humanFileSize } from "@/utils/common";
import { displayName } from "@/utils/auth";
import Confirm from "@/components/Confirm";
import { useStore } from "vuex";
import { computed } from "@vue/runtime-core";

export default {
  components: { UserTable, Confirm },
  setup: () => {
    const store = useStore();
    const nginxLimit = computed(() => store.getters["config/uploadLimit"]);
    const { save, loading } = useMutation(userGraph.updateUser);
    const saveUploadLimit = async (user, close) => {
      await save(
        `Successfully change ${displayName(
          user
        )}'s upload limit to ${humanFileSize(user.uploadLimit)}!`,
        user
      );
      close();
    };

    return { loading, saveUploadLimit, humanFileSize, nginxLimit };
  },
};
</script>

<style>
</style>