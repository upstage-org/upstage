<template>
  <div class="columns">
    <div class="column">
      <Field horizontal v-model="form.name" label="Media Name" />
      <MediaType v-model="form.mediaType" />
      <Tabs :items="tabs" :centered="true">
        <template #preview>
          <div style="text-align: center">
            <Asset :asset="media" />
          </div>
        </template>
        <template #voice>
          <VoiceParameters v-model="form.voice" />
        </template>
        <template #multiframe>
          <HorizontalField title="Multiframe">
            <Switch v-model="form.multi" className="is-rounded is-success" />
          </HorizontalField>
          <HorizontalField v-if="form.multi">
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
        </template>
      </Tabs>
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
import Tabs from "@/components/Tabs";
import VoiceParameters from "@/components/stage/SettingPopup/settings/VoiceParameters";

export default {
  components: {
    HorizontalField,
    Field,
    MediaType,
    SaveButton,
    Switch,
    Asset,
    MultiSelectList,
    Tabs,
    VoiceParameters,
  },
  props: {
    media: Object,
  },
  setup: (props) => {
    const form = reactive(props.media);
    form.mediaType = form.assetType.name;
    form.multi = false;
    form.frames = [];
    form.voice = {};
    if (form.description) {
      Object.assign(form, JSON.parse(form.description));
    }
    const refresh = inject("refresh");

    const { loading, save } = useMutation(stageGraph.updateMedia);
    const updateMedia = async () => {
      const { id, name, mediaType, multi, frames, voice } = form;
      const payload = {
        id,
        name,
        mediaType,
        description: JSON.stringify({ multi, frames, voice }),
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

    const tabs = computed(() => {
      const res = [{ key: "preview", label: "Preview", icon: "fas fa-image" }];
      if (form.mediaType === "avatar") {
        res.push({ key: "voice", label: "Voice", icon: "fas fa-volume-up" });
      }
      if (form.mediaType === "avatar" || form.mediaType === "prop") {
        res.push({
          key: "multiframe",
          label: "Multiframe",
          icon: "fas fa-clone",
        });
      }
      return res;
    });

    return {
      form,
      loading,
      updateMedia,
      allMedia,
      loadingAllMedia,
      availableTypes,
      tabs,
    };
  },
};
</script>

<style>
</style>