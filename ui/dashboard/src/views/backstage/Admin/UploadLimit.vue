<template>
  <Confirm
    @confirm="(close) => saveUploadLimit(item, close)"
    :loading="loading"
  >
    <template #render="{ confirm }">
      <input
        class="slider is-fullwidth m-0"
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

<script>
import { useMutation } from "@/services/graphql/composable";
import { userGraph } from "@/services/graphql";
import { humanFileSize } from "@/utils/common";
import { displayName } from "@/utils/auth";
import Confirm from "@/components/Confirm";
import { useStore } from "vuex";
import { computed } from "@vue/runtime-core";

export default {
  components: { Confirm },
  props: ["user", "displayName"],
  setup: (props) => {
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

    return {
      loading,
      saveUploadLimit,
      humanFileSize,
      nginxLimit,
      item: props.user,
    };
  },
};
</script>

<style>
</style>