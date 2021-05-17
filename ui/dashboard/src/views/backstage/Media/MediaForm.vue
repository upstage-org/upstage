<template>
  <div class="columns">
    <div class="column is-narrow has-text-centered" style="max-width: 20vw">
      <Asset :asset="media" />
    </div>
    <div class="column">
      <Field horizontal v-model="form.name" label="Media Name" />
      <MediaType v-model="form.mediaType" />
      <HorizontalField v-if="multiframable" title="Multiframe">
        <Switch v-model="form.multi" className="is-rounded is-success" />
      </HorizontalField>
      <HorizontalField v-if="multiframable && form.multi">
        <MultiSelectList
          :loading="loadingAllMedia"
          :data="
            allMedia
              ?.filter((item) => item.assetType.name !== 'audio')
              .map((media) => media.fileLocation)
          "
          v-model="form.frames"
          :columnClass="() => 'is-4'"
        >
          <template #render="{ item: fileLocation }">
            <Asset :asset="{ fileLocation }" />
          </template>
        </MultiSelectList>
      </HorizontalField>
    </div>
  </div>
  <SaveButton @click="updateMedia" :loading="loading" :disabled="!form.name" />
</template>

<script>
import { reactive } from "@vue/reactivity";
import { useMutation, useQuery } from "@/services/graphql/composable";
import { stageGraph } from "@/services/graphql";
import { computed, inject } from "@vue/runtime-core";
import { notification } from "@/utils/notification";
import HorizontalField from "@/components/form/HorizontalField";
import Field from "@/components/form/Field";
import MediaType from "@/components/form/MediaType";
import SaveButton from "@/components/form/SaveButton";
import Switch from "@/components/form/Switch";
import Asset from "@/components/Asset";
import MultiSelectList from "@/components/MultiSelectList";

export default {
  components: {
    HorizontalField,
    Field,
    MediaType,
    SaveButton,
    Switch,
    Asset,
    MultiSelectList,
  },
  props: {
    media: Object,
  },
  setup: (props) => {
    const form = reactive(props.media);
    form.mediaType = form.assetType.name;
    if (form.description) {
      Object.assign(form, JSON.parse(form.description));
    } else {
      form.multi = false;
      form.frames = [];
    }
    const refresh = inject("refresh");

    const multiframable = computed(
      () => form.mediaType === "avatar" || form.mediaType === "prop"
    );

    const { loading, save } = useMutation(stageGraph.updateMedia);
    const updateMedia = async () => {
      const { id, name, mediaType, multi, frames } = form;
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
    const availableTypes = computed(() => {
      if (form.fileType === "image") return ["avatar", "prop", "backdrop"];
      if (form.fileType === "audio") return ["audio"];
      if (form.fileType === "video") return ["stream"];
    });

    return {
      form,
      loading,
      updateMedia,
      allMedia,
      loadingAllMedia,
      multiframable,
      availableTypes,
    };
  },
};
</script>

<style>
</style>