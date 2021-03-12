<template>
  <Modal>
    <template #trigger>
      <span class="icon">
        <i class="fas fa-pen" aria-hidden="true"></i>
      </span>
    </template>
    <template #header> Edit {{ data.name }} </template>
    <template #content>
      <Field horizontal v-model="data.name" label="Media Name" />
      <HorizontalField title="Type">
        <div class="control">
          <label class="radio">
            <input type="radio" v-model="data.mediaType" value="avatar" />
            Avatar
          </label>
          <label class="radio">
            <input type="radio" v-model="data.mediaType" value="prop" />
            Prop
          </label>
          <label class="radio">
            <input type="radio" v-model="data.mediaType" value="backdrop" />
            Backdrop
          </label>
          <label class="radio">
            <input type="radio" v-model="data.mediaType" value="audio" />
            Audio
          </label>
        </div>
      </HorizontalField>
    </template>
    <template #footer>
      <SaveButton
        @click="updateMedia"
        :loading="loading"
        :disabled="!data.name"
      />
    </template>
  </Modal>
  <div></div>
</template>

<script>
import HorizontalField from "@/components/form/HorizontalField";
import Field from "@/components/form/Field";
import Modal from "@/components/Modal";
import SaveButton from "@/components/form/SaveButton";
import { reactive } from "@vue/reactivity";
import { useMutation } from "@/services/graphql/composable";
import { stageGraph } from "@/services/graphql";
import { inject } from "@vue/runtime-core";
import { notification } from "@/utils/notification";

export default {
  components: { HorizontalField, Field, Modal, SaveButton },
  props: {
    media: Object,
  },
  setup: (props) => {
    const data = reactive(props.media);
    const refresh = inject("refresh");

    const { loading, save } = useMutation(stageGraph.updateMedia);
    const updateMedia = async () => {
      console.log(data);
      await save(() => {
        notification.success("Media updated successfully!");
        refresh();
      }, data);
    };

    return { data, loading, updateMedia };
  },
};
</script>

<style>
.field-label {
  padding-top: 0 !important;
}
</style>