<template>
  <section class="hero is-small is-light is-bold">
    <div class="hero-body">
      <h1 class="title is-inline">Media</h1>
      &nbsp;
      <MediaUpload @complete="fetch" />
    </div>
  </section>
  <div class="columns">
    <div class="column is-4">
      <aside class="menu box has-background-light mx-4">
        <ul class="menu-list">
          <Skeleton v-if="loadingTypes" />
          <template v-else>
            <li v-for="type in types" :key="type">
              <a
                @click="mediaType = type"
                class="type-name"
                :class="{
                  'is-active':
                    mediaType === type ||
                    (!mediaType.name && type.name === 'media'),
                }"
              >
                {{ type.name }}
              </a>
            </li>
          </template>
        </ul>
      </aside>
    </div>
    <div class="column is-8">
      <div class="pt-4 pr-4 pb-4">
        <Skeleton v-if="loading" />
        <MediaList v-else />
      </div>
    </div>
  </div>
</template>

<script>
import MediaList from "./MediaList";
import MediaUpload from "@/components/MediaUpload";
import Skeleton from "@/components/Skeleton";
import { provide, ref, watchEffect } from "@vue/runtime-core";
import { stageGraph } from "@/services/graphql";
import { useQuery } from "@/services/graphql/composable";

export default {
  components: { MediaList, MediaUpload, Skeleton },
  setup: () => {
    const mediaType = ref({});
    const { loading, nodes: mediaList, fetch } = useQuery(stageGraph.mediaList);
    provide("mediaList", mediaList);
    provide("loading", loading);
    const refresh = () => {
      const assetTypeId =
        mediaType.value.name === "media" ? null : mediaType.value.dbId;
      fetch({
        assetTypeId,
      });
    };
    provide("refresh", refresh);

    watchEffect(refresh);

    const { loading: loadingTypes, nodes: types } = useQuery(
      stageGraph.assetTypeList
    );

    return { fetch, loading, loadingTypes, types, mediaType };
  },
};
</script>

<style>
.type-name {
  text-transform: capitalize;
}
</style>