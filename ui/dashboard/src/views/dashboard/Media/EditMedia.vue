<template>
  <Modal width="100%">
    <template #trigger>
      <span class="icon">
        <i class="fas fa-pen" aria-hidden="true"></i>
      </span>
    </template>
    <template #header> Edit {{ data.name }} </template>
    <template #content>
      <div class="columns">
        <div class="column is-narrow has-text-centered" style="max-width: 20vw">
          <Asset :asset="media" />
        </div>
        <div class="column">
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
          <HorizontalField v-if="multiframable" title="Multiframe">
            <Switch v-model="data.multi" className="is-rounded is-success" />
          </HorizontalField>
          <HorizontalField v-if="multiframable && data.multi">
            <MultiSelectList
              :loading="loadingAllMedia"
              :data="
                allMedia
                  .filter((item) => item.assetType.name !== 'audio')
                  .map((media) => media.fileLocation)
              "
              v-model="data.frames"
              :columnClass="() => 'is-4'"
            >
              <template #render="{ item: fileLocation }">
                <Asset :asset="{ fileLocation }" />
              </template>
            </MultiSelectList>
          </HorizontalField>
        </div>
      </div>
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
import Switch from "@/components/form/Switch";
import Asset from "@/components/Asset";
import { reactive } from "@vue/reactivity";
import { useMutation, useQuery } from "@/services/graphql/composable";
import { stageGraph } from "@/services/graphql";
import { computed, inject } from "@vue/runtime-core";
import { notification } from "@/utils/notification";
import MultiSelectList from "@/components/MultiSelectList";

export default {
  components: {
    HorizontalField,
    Field,
    Modal,
    SaveButton,
    Switch,
    Asset,
    MultiSelectList,
  },
  props: {
    media: Object,
  },
  setup: (props) => {
    const data = reactive(props.media);
    data.mediaType = data.assetType.name;
    if (data.description) {
      Object.assign(data, JSON.parse(data.description));
    } else {
      data.multi = false;
      data.frames = [];
    }
    const refresh = inject("refresh");

    const multiframable = computed(
      () => data.mediaType === "avatar" || data.mediaType === "prop"
    );

    const { loading, save } = useMutation(stageGraph.updateMedia);
    const updateMedia = async () => {
      const { id, name, mediaType, multi, frames } = data;
      const payload = {
        id,
        name,
        mediaType,
        description: JSON.stringify({ multi, frames }),
      };
      await save(() => {
        notification.success("Media updated successfully!");
        refresh();
      }, payload);
    };

    const { nodes: allMedia, loading: loadingAllMedia } = useQuery(
      stageGraph.mediaList
    );

    return {
      data,
      loading,
      updateMedia,
      allMedia,
      loadingAllMedia,
      multiframable,
    };
  },
};
</script>

<style>
.field-label {
  padding-top: 0 !important;
  white-space: nowrap;
}
</style>