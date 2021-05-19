<template>
  <section class="modal-card-body p-0">
    <button
      class="delete close-modal"
      aria-label="close"
      @click="closeModal"
    ></button>
    <div class="container-fluid">
      <Tabs :items="tabs" teleport="#header">
        <template #preview>
          <div style="text-align: center; height: calc(100vh - 200px)">
            <Asset :asset="media" />
          </div>
        </template>
        <template #stages>
          <MultiSelectList
            :loading="loadingAllMedia"
            :data="stageList"
            v-model="form.stages"
            :columnClass="() => 'is-12'"
          >
            <template #render="{ item }">
              <div class="box m-0">
                <div class="content">
                  <strong>{{ item.name }}</strong>
                  <span style="float: right">
                    Created by
                    <span class="has-text-primary">
                      {{ displayName(item.owner) }}
                    </span>
                  </span>
                  <br />
                  <small>{{ item.description }}</small>
                </div>
              </div>
            </template>
          </MultiSelectList>
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
  </section>
  <footer class="modal-card-foot">
    <div class="columns is-fullwidth">
      <div class="column">
        <Field horizontal v-model="form.name" label="Media Name" />
      </div>
      <div class="column is-narrow">
        <Field horizontal label="Media Type">
          <MediaType v-model="form.mediaType" />
        </Field>
      </div>
      <div class="column is-narrow">
        <SaveButton @click="save" :loading="loading" :disabled="!form.name" />
      </div>
    </div>
  </footer>
</template>

<script>
import { reactive, ref } from "@vue/reactivity";
import { useMutation, useQuery } from "@/services/graphql/composable";
import { stageGraph } from "@/services/graphql";
import { computed, inject, watch } from "@vue/runtime-core";
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
import { displayName } from "@/utils/auth";

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

    const { mutation: updateMedia } = useMutation(stageGraph.updateMedia);
    const { mutation: assignStages } = useMutation(stageGraph.assignStages);

    const loading = ref(false);
    const save = async () => {
      try {
        loading.value = true;
        const { id, name, mediaType, multi, frames, voice } = form;
        const stageIds = form.stages.map((s) => s.dbId);
        const payload = {
          id,
          name,
          mediaType,
          description: JSON.stringify({ multi, frames, voice }),
        };
        await Promise.all([updateMedia(payload), assignStages(id, stageIds)]);
        notification.success("Media updated successfully!");
        refresh();
      } catch (error) {
        notification.error(error);
      } finally {
        loading.value = false;
      }
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
      const res = [
        { key: "preview", label: "Preview", icon: "fas fa-image" },
        { key: "stages", label: "Stage", icon: "fas fa-person-booth" },
      ];
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
    const { nodes: stageList } = useQuery(stageGraph.stageList);
    watch(
      stageList,
      (val) => {
        if (val) {
          form.stages = form.stages.map((stage) =>
            val.find((s) => s.dbId === stage.id)
          );
          console.log(form.stages);
        }
      },
      { immediate: true }
    );

    const closeModal = inject("closeModal");

    return {
      form,
      loading,
      save,
      allMedia,
      loadingAllMedia,
      availableTypes,
      tabs,
      stageList,
      displayName,
      closeModal,
    };
  },
};
</script>

<style lang="scss" scoped>
.close-modal {
  position: absolute;
  right: 20px;
  top: 10px;
  z-index: 20;
}

::v-deep .field-label {
  white-space: nowrap;
  margin: auto;
  margin-right: 10px;
}
</style>