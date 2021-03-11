<template>
  <SaveButton class="mb-4" :loading="saving" @click="saveMedia" />
  <MultiSelectList
    :loading="loading"
    :titles="['Available Media', 'Selected Media']"
    :data="mediaList"
    v-model="selectedMedia"
  >
    <template #render="{ item }">
      <span class="tag is-light is-small type-tag">
        {{ item.assetType.name }}
      </span>
      <div class="card-image">
        <Asset :asset="item" />
      </div>
      <header class="card-header">
        <p class="card-header-title">{{ item.name }}</p>
      </header>
    </template>
  </MultiSelectList>
</template>

<script>
import MultiSelectList from "@/components/MultiSelectList";
import Asset from "@/components/Asset";
import SaveButton from "@/components/form/SaveButton";
import { stageGraph } from "@/services/graphql";
import {
  useAttribute,
  useMutation,
  useQuery,
} from "@/services/graphql/composable";
import { ref } from "@vue/reactivity";
import { inject, watchEffect } from "@vue/runtime-core";
export default {
  components: { MultiSelectList, Asset, SaveButton },
  setup: () => {
    const stage = inject("stage");
    const selectedMedia = ref([]);
    const { loading, nodes: mediaList } = useQuery(stageGraph.mediaList);
    const { loading: saving, save } = useMutation(stageGraph.saveStageMedia);

    watchEffect(() => {
      const savedMedia = useAttribute(stage, "media", true);
      if (!savedMedia.value || !mediaList.value) return;
      selectedMedia.value = mediaList.value.filter((media) => {
        return savedMedia.value.some((m) => m.src === media.fileLocation);
      });
    });

    const saveMedia = async () => {
      const payload = JSON.stringify(
        selectedMedia.value.map((media) => ({
          name: media.name,
          type: media.assetType.name,
          src: media.fileLocation,
        }))
      );
      await save("Media saved successfully!", stage.value.id, payload);
    };

    return { loading, mediaList, selectedMedia, saveMedia, saving };
  },
};
</script>

<style>
</style>