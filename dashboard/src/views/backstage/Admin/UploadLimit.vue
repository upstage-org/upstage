<template>
  <Confirm
    @confirm="(close) => saveUploadLimit(item, close)"
    :loading="loading"
  >
    <template #render="{ confirm }">
      <Dropdown
        :data="limitSize"
        :render-label="(item) => item.label"
        :render-value="(item) => item.value"
        v-model="item.uploadLimit"
        :isUp="item.lastItem"
        @update:model-value="
          item.selectSize = $event;
          confirm();
        "
      />
    </template>
    Are you sure you want to change {{ displayName }}'s upload limit to<br />
    <span class="has-text-danger">
      {{ humanFileSize(item.selectSize) }}
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
import { UPDATE_LIMIT } from "@/utils/constants";
import Dropdown from "@/components/form/Dropdown.vue";

export default {
  components: { Confirm, Dropdown },
  props: ["user", "displayName"],
  setup: (props) => {
    const store = useStore();
    const nginxLimit = computed(() => store.getters["config/uploadLimit"]);
    const limitSize = [];

    for (let item in UPDATE_LIMIT) {
      limitSize.push({
        label: humanFileSize(UPDATE_LIMIT[item]),
        value: UPDATE_LIMIT[item],
      });
    }

    limitSize.push({
      label: humanFileSize(nginxLimit.value),
      value: nginxLimit.value,
    });

    const { save, loading } = useMutation(userGraph.updateUser);
    const saveUploadLimit = async (user, close) => {
      user.uploadLimit = user.selectSize;
      await save(
        `Successfully change ${displayName(
          user,
        )}'s upload limit to ${humanFileSize(user.uploadLimit)}!`,
        user,
      );
      close();
    };

    return {
      limitSize,
      loading,
      saveUploadLimit,
      humanFileSize,
      nginxLimit,
      item: props.user,
    };
  },
};
</script>

<style></style>
