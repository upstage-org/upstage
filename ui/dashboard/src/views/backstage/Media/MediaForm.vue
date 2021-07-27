<template>
  <section class="modal-card-body p-0">
    <button
      class="delete close-modal"
      aria-label="close"
      @click="closeModal"
    ></button>
    <div class="container-fluid">
      <Tabs :items="tabs">
        <template #preview>
          <div class="preview">
            <div v-if="!media.isRTMP">
              <Asset :asset="media" @detect-size="updateMediaSize" />
              <Upload
                v-if="!active"
                v-model="form.base64"
                :type="fileType"
                :preview="false"
                @change="handleFileChange"
              >
                <span>Replace</span>
                <span class="icon">
                  <i class="fas fa-retweet"></i>
                </span>
              </Upload>
            </div>
            <template v-else>
              <RTMPStream controls :src="media.src" />
              <Field
                horizontal
                label="Unique key"
                v-model="form.src"
                help="You can change it to anything you like, but remember: it must be unique!"
              />
              <p>
                Use this URL to publish your stream:
                <a :href="getPublishLink(form.src)">{{
                  getPublishLink(form.src)
                }}</a>
              </p>
              <OBSInstruction :src="form.src" />
            </template>
          </div>
        </template>
        <template #copyright>
          <HorizontalField title="Copyright Level">
            <Dropdown
              v-model="form.copyrightLevel"
              :data="copyrightLevels"
              :render-label="(item) => item.name"
              :render-value="(item) => item.value"
              :render-description="(item) => item.description"
            />
          </HorizontalField>
          <HorizontalField v-show="[2].includes(form.copyrightLevel)">
            <div style="margin-right: 32px">
              <MultiTransferColumn
                :columns="['No access', 'Readonly access', 'Editor access']"
                :data="users"
                :renderLabel="displayName"
                :renderValue="(item) => item.dbId"
                :renderKeywords="
                  (item) =>
                    `${item.firstName} ${item.lastName} ${item.username} ${item.email} ${item.displayName}`
                "
                v-model="playerAccess"
              />
            </div>
          </HorizontalField>
        </template>
        <template #stages>
          <MultiSelectList
            :loading="loadingAllMedia"
            :data="availableStages"
            v-model="form.assignedStages"
            :columnClass="() => 'is-12 p-0'"
          >
            <template #render="{ item }">
              <div class="box m-0 p-2">
                <div class="content">
                  <strong>{{ item.name }}</strong>
                  <span style="float: right">
                    Created by
                    <span class="has-text-primary">
                      {{ displayName(item.owner) }}
                    </span>
                  </span>
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
                  .map((media) => media.src)
              "
              v-model="form.frames"
              :columnClass="() => 'is-4'"
            >
              <template #render="{ item: src }">
                <Asset :asset="{ src }" />
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
          <button v-if="media.isRTMP" class="button" disabled>Stream</button>
          <MediaType
            v-else
            v-model="form.mediaType"
            :data="availableTypes"
            is-up
          />
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
import { stageGraph, userGraph } from "@/services/graphql";
import { computed, inject, watch } from "@vue/runtime-core";
import { notification } from "@/utils/notification";
import HorizontalField from "@/components/form/HorizontalField";
import Field from "@/components/form/Field";
import MediaType from "@/components/form/MediaType";
import SaveButton from "@/components/form/SaveButton";
import Switch from "@/components/form/Switch";
import Upload from "@/components/form/Upload";
import Dropdown from "@/components/form/Dropdown";
import Asset from "@/components/Asset";
import MultiSelectList from "@/components/MultiSelectList";
import Tabs from "@/components/Tabs";
import RTMPStream from "@/components/RTMPStream";
import MultiTransferColumn from "@/components/MultiTransferColumn";
import VoiceParameters from "@/components/stage/SettingPopup/settings/VoiceParameters";
import { displayName } from "@/utils/auth";
import { getPublishLink } from "@/utils/streaming";
import OBSInstruction from "./OBSInstruction";
import { MEDIA_COPYRIGHT_LEVELS } from "@/utils/constants";

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
    RTMPStream,
    OBSInstruction,
    Upload,
    MultiTransferColumn,
    Dropdown,
  },
  props: {
    media: Object,
  },
  methods: {
    getPublishLink,
  },
  emits: ["complete"],
  setup: (props, { emit }) => {
    const form = reactive(props.media);
    form.multi = false;
    form.frames = [];
    form.voice = {};
    if (form.description) {
      Object.assign(form, JSON.parse(form.description));
    }
    if (form.assetType) {
      form.mediaType = form.assetType.name;
    }
    if (form.isRTMP && !form.src) {
      form.src = form.fileLocation;
    }

    const { mutation: uploadMedia } = useMutation(stageGraph.uploadMedia);
    const { mutation: updateMedia } = useMutation(stageGraph.updateMedia);
    const { mutation: assignStages } = useMutation(stageGraph.assignStages);

    const loading = ref(false);
    const save = async () => {
      try {
        loading.value = true;
        const {
          name,
          base64,
          mediaType,
          filename,
          copyrightLevel,
          playerAccess,
        } = form;
        let message = "Media updated successfully!";
        if (!form.id) {
          if (form.isRTMP) {
            const response = await updateMedia({
              name,
              mediaType,
              fileLocation: form.src,
              copyrightLevel,
              playerAccess,
            });
            Object.assign(form, response.updateMedia.asset);
          } else {
            const response = await uploadMedia({
              name,
              base64,
              mediaType,
              filename,
            });
            Object.assign(form, response.uploadMedia.asset);
          }
          message = "Media created successfully!";
        }
        const stageIds = form.assignedStages.map((s) => s.dbId);
        const { id, multi, frames, voice, isRTMP, src, w, h } = form;
        const payload = {
          id,
          name,
          mediaType,
          base64,
          description: JSON.stringify({
            multi,
            frames,
            voice,
            isRTMP,
            w,
            h,
          }),
          fileLocation: src,
          copyrightLevel,
          playerAccess,
        };
        await Promise.all([updateMedia(payload), assignStages(id, stageIds)]);
        notification.success(message);
        emit("complete", form);
        closeModal();
      } catch (error) {
        notification.error(error);
      } finally {
        loading.value = false;
      }
    };

    const { nodes: allMedia, loading: loadingAllMedia } = useQuery(
      stageGraph.mediaList
    );
    const fileType = computed(() => {
      if (["avatar", "prop", "backdrop", "curtain"].includes(form.mediaType)) {
        return "image";
      }
      if (["audio"].includes(form.mediaType)) {
        return "audio";
      }
      if (["stream"].includes(form.mediaType)) {
        return "video";
      }
    });
    const availableTypes = computed(() => {
      const type = form.fileType ?? fileType.value;
      if (type === "image") return ["avatar", "prop", "backdrop", "curtain"];
      if (type === "audio") return ["audio"];
      if (type === "video") return ["stream"];
    });

    const tabs = computed(() => {
      const res = [
        { key: "preview", label: "Preview", icon: "fas fa-image" },
        { key: "copyright", label: "Copyright", icon: "fas fa-copyright" },
      ];
      if (!["curtain"].includes(form.mediaType)) {
        res.push({
          key: "stages",
          label: "Stage",
          icon: "fas fa-person-booth",
        });
      }
      if (form.mediaType === "avatar") {
        res.push({ key: "voice", label: "Voice", icon: "fas fa-volume-up" });
      }
      if (
        form.mediaType === "avatar" ||
        form.mediaType === "prop" ||
        form.mediaType === "backdrop"
      ) {
        res.push({
          key: "multiframe",
          label: "Multiframe",
          icon: "fas fa-clone",
        });
      }
      return res;
    });
    const { nodes: stageList } = useQuery(stageGraph.stageList);
    const availableStages = computed(() => {
      if (!stageList.value) return [];
      const res = stageList.value.filter(
        (stage) => stage.permission === "owner" || stage.permission === "editor"
      );
      res.sort((a, b) => (a.name > b.name ? 1 : -1));
      return res;
    });
    watch(
      stageList,
      (val) => {
        if (val) {
          form.assignedStages = form.stages.map((stage) =>
            val.find((s) => s.dbId === stage.id)
          );
        } else {
          form.assignedStages = [];
        }
      },
      { immediate: true }
    );

    const closeModal = inject("closeModal");

    const updateMediaSize = ({ width, height }) => {
      if (width > height) {
        form.w = 100;
        form.h = (100 * height) / width;
      } else {
        form.h = 100;
        form.w = (100 * width) / height;
      }
    };

    const copyrightLevels = MEDIA_COPYRIGHT_LEVELS;
    const { nodes: users } = useQuery(userGraph.userList);
    const playerAccess = ref(
      form.playerAccess ? JSON.parse(form.playerAccess) : []
    );
    watch(playerAccess, (val) => {
      form.playerAccess = JSON.stringify(val);
    });

    return {
      form,
      loading,
      save,
      allMedia,
      loadingAllMedia,
      availableTypes,
      tabs,
      availableStages,
      displayName,
      closeModal,
      updateMediaSize,
      fileType,
      copyrightLevels,
      users,
      playerAccess,
    };
  },
};
</script>

<style lang="scss" scoped>
:deep(.field-label) {
  white-space: nowrap;
  margin: auto;
  margin-right: 10px;
}

:deep(.file) {
  justify-content: center;
}

.close-modal {
  position: absolute;
  right: 20px;
  top: 10px;
  z-index: 20;
}

.preview {
  text-align: center;
  height: calc(100vh - 200px);
  padding: 24px;

  .field {
    text-align: left;
  }
}
</style>