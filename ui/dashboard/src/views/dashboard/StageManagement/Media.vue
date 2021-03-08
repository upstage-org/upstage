<template>
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
import { stageGraph } from "@/services/graphql";
import { useQuery } from "@/services/graphql/composable";
import { ref } from "@vue/reactivity";
export default {
  components: { MultiSelectList, Asset },
  setup: () => {
    const selectedMedia = ref([]);
    const { loading, nodes: mediaList } = useQuery(stageGraph.mediaList);

    return { loading, mediaList, selectedMedia };
  },
};
</script>

<style>
</style>