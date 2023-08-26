<template>
  <div class="columns">
    <div class="column">
      <button
        class="button mr-2 is-dark"
        :class="{ 'is-warning': reordering }"
        @click="reordering = !reordering"
      >
        <span class="icon">
          <i class="fas fa-arrow-left" v-if="reordering"></i>
          <i class="fas fa-arrows-alt" v-else></i>
        </span>
        <span v-if="reordering">{{ $t("exit_reorder_mode") }}</span>
        <span v-else>{{ $t("reorder_mode") }}</span>
      </button>
      <template v-if="!reordering">
        <Dropdown
          class="mr-2"
          v-model="filter.type"
          :data="mediaTypes"
          :render-value="(item) => item.value"
          :render-label="(item) => item.label"
          placeholder="Media type"
        />
        <Dropdown
          class="mr-2"
          v-model="filter.owner"
          :data="owners.concat({ displayName: 'All players' })"
          :render-value="(item) => item.id"
          :render-label="displayName"
          placeholder="Stage owner"
        />
        <Field
          style="width: 200px; display: inline-block; vertical-align: top"
          v-model="filter.keyword"
          right="fas fa-search"
          placeholder="Media name"
        />
      </template>
    </div>
    <div class="column is-narrow">
      <SaveButton :loading="saving" :disabled="loading" @click="saveMedia" />
    </div>
  </div>

  <Reorder v-if="reordering" v-model="selectedMedia" />
  <MultiSelectList
    v-else
    :loading="loading"
    :titles="['Available Media', `Media assigned to this Stage`]"
    :data="filteredMediaList"
    :sizeTotal="totalSize"
    :column-class="() => 'is-12'"
    v-model="selectedMedia"
  >
    <template #render="{ item }">
      <div class="mx-3 my-1">
        <div class="columns">
          <div class="column is-narrow media-preview">
            <Asset
              v-if="!['audio', 'stream'].includes(item.mediaType)"
              :asset="item"
              show-type
            />
          </div>
          <div class="type-icon">
            <Icon :src="item.mediaType + '.svg'" />
          </div>
          <div class="column">{{ item.name }}</div>
          <div class="column has-text-right has-text-grey-dark">
            <small>{{ $t("created_by") }}</small>
            {{ displayName(item.owner) }}
          </div>
        </div>
        <div class="columns px-1">
          <MultiframePreview :asset="item" />
        </div>
      </div>
    </template>
  </MultiSelectList>
</template>

<script>
import MultiSelectList from "@/components/MultiSelectList";
import Asset from "@/components/Asset";
import SaveButton from "@/components/form/SaveButton";
import Dropdown from "@/components/form/Dropdown";
import Field from "@/components/form/Field";
import Icon from "@/components/Icon";
import { stageGraph } from "@/services/graphql";
import {
  useMutation,
  useOwners,
  useQuery,
} from "@/services/graphql/composable";
import { reactive, ref } from "@vue/reactivity";
import { computed, inject, watch, watchEffect } from "@vue/runtime-core";
import { displayName } from "@/utils/auth";
import { includesIgnoreCase } from "@/utils/common";
import { useStore } from "vuex";
import MultiframePreview from "../Media/MultiframePreview";
import Reorder from "./Reorder.vue";

export default {
  components: {
    MultiSelectList,
    Asset,
    SaveButton,
    Dropdown,
    Icon,
    Field,
    MultiframePreview,
    Reorder,
  },
  setup: () => {
    const store = useStore();
    const stage = inject("stage");
    const selectedMedia = ref([]);
    const totalSize = ref(0);
    const { loading, data } = useQuery(stageGraph.assignableMedia);
    const { loading: saving, save } = useMutation(stageGraph.saveStageMedia);

    const mediaList = computed(() => {
      if (!data.value) return [];
      const { avatars, props, backdrops, audios, streams, curtains } =
        data.value;
      const mediaList = []
        .concat(
          avatars.edges,
          props.edges,
          backdrops.edges,
          audios.edges,
          streams.edges,
          curtains.edges,
        )
        .map((edge) => edge.node);
      return mediaList;
    });

    watchEffect(() => {
      if (!stage.value || !mediaList.value) return;
      selectedMedia.value = stage.value.media.map((m) =>
        mediaList.value.find((media) => media.dbId === m.id),
      );
      if (selectedMedia.value[0]) {
        totalSize.value = selectedMedia?.value.reduce(
          (accumulator, currentValue) => accumulator + currentValue.size,
          0,
        );
      }
    });

    const saveMedia = async () => {
      const ids = selectedMedia.value.map((media) => media.dbId);
      await save("Stage updated successfully!", stage.value.id, ids);
    };

    const mediaTypes = [
      { label: "All media", value: undefined },
      {
        label: "Avatar",
        value: "avatar",
      },
      {
        label: "Prop",
        value: "prop",
      },
      {
        label: "Backdrop",
        value: "backdrop",
      },
      { label: "Audio", value: "audio" },
      { label: "Stream", value: "stream" },
      { label: "Curtain", value: "curtain" },
    ];
    const filter = reactive({});
    const filteredMediaList = computed(() => {
      let list = mediaList.value;
      if (filter.type) {
        list = list.filter((media) => media.assetType.name === filter.type);
      }
      if (filter.owner) {
        list = list.filter((media) => media.owner.id === filter.owner);
      }
      if (filter.keyword) {
        list = list.filter((media) =>
          includesIgnoreCase(media.name, filter.keyword),
        );
      }
      return list;
    });

    const owners = useOwners(mediaList);
    watch(owners, (val) => {
      const current = store.getters["user/currentUserId"];
      if (val.find((owner) => owner.id === current)) {
        filter.owner = current;
      }
    });

    const reordering = ref(false);

    return {
      loading,
      mediaList,
      selectedMedia,
      saveMedia,
      saving,
      mediaTypes,
      filter,
      filteredMediaList,
      displayName,
      owners,
      reordering,
      totalSize,
    };
  },
};
</script>

<style scoped lang="scss">
.media-preview {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0;
  width: 48px;
  height: 48px;
  border-radius: 5px;
  overflow: hidden;
}
.type-icon {
  align-self: center;
  padding: 0 16px;
}
</style>
