<template>
  <section class="hero is-small is-dark is-bold">
    <div class="hero-body">
      <Breadcrumb description="Upload and manage media" />
      <h1 class="title is-inline">Media</h1>
      &nbsp;
      <MediaUpload :special="true" v-if="!isGuest" />
    </div>
  </section>
  <div class="columns">
    <div class="column is-3">
      <aside class="menu box has-background-light mx-4">
        <Skeleton v-if="loadingTypes" />
        <template v-else>
          <p class="menu-label">Media Name</p>
          <p>
            <Field v-model="filter.name" right="fas fa-filter" />
          </p>
          <p class="menu-label">Media Type</p>
          <ul class="menu-list">
            <li v-for="type in types" :key="type">
              <a
                @click="filter.mediaType = type"
                class="type-name"
                :class="{
                  'is-active':
                    filter.mediaType === type ||
                    (!filter.mediaType && type.name === 'media'),
                }"
              >
                {{ type.name === "media" ? "All Media" : type.name }}
              </a>
            </li>
          </ul>
          <p class="menu-label">Owner</p>
          <ul class="menu-list">
            <li @click="filter.owner = null">
              <a :class="{ 'is-active': filter.owner === null }">All Users</a>
            </li>
            <li v-for="user in users" :key="user" @click="filter.owner = user">
              <a :class="{ 'is-active': filter.owner === user }">{{
                displayName(user)
              }}</a>
            </li>
          </ul>
          <p class="menu-label">Stage</p>
          <ul class="menu-list">
            <li @click="filter.stage = null">
              <a :class="{ 'is-active': filter.stage === null }">All Stages</a>
            </li>
            <li
              v-for="stage in stageList"
              :key="stage"
              @click="filter.stage = stage"
            >
              <a :class="{ 'is-active': filter.stage === stage }">
                {{ stage.name }}
              </a>
            </li>
          </ul>
        </template>
      </aside>
    </div>
    <div class="column is-9">
      <div class="pt-4 pr-4 pb-4">
        <Skeleton v-if="loading" />
        <MediaList v-else />
      </div>
    </div>
  </div>
</template>

<script>
import MediaList from "./MediaList";
import MediaUpload from "./MediaUpload";
import Skeleton from "@/components/Skeleton";
import Field from "@/components/form/Field";
import { computed, provide, reactive } from "@vue/runtime-core";
import { stageGraph } from "@/services/graphql";
import { useOwners, useQuery } from "@/services/graphql/composable";
import { displayName } from "@/utils/auth";
import Breadcrumb from "@/components/Breadcrumb";
import { useStore } from "vuex";

export default {
  components: { MediaList, MediaUpload, Skeleton, Field, Breadcrumb },
  setup: () => {
    const store = useStore();
    const isGuest = computed(() => store.getters["user/isGuest"]);

    const filter = reactive({
      mediaType: null,
      owner: null,
    });
    const { loading, nodes, fetch, refresh, popNode } = useQuery(
      stageGraph.mediaList
    );

    const users = useOwners(nodes);

    const { nodes: stageList } = useQuery(stageGraph.stageList);

    const mediaList = computed(() => {
      let list = nodes.value;
      if (filter.name) {
        list = list.filter((media) =>
          media.name.toLowerCase().includes(filter.name.toLowerCase())
        );
      }
      if (
        filter.mediaType &&
        filter.mediaType.name &&
        filter.mediaType.name !== "media"
      ) {
        list = list.filter(
          (media) => media.assetType.name === filter.mediaType.name
        );
      }
      if (filter.owner) {
        list = list.filter(
          (media) => media.owner.username === filter.owner.username
        );
      }
      if (filter.stage) {
        list = list.filter((media) =>
          media.stages.find((s) => s.id === filter.stage.dbId)
        );
      }
      return list;
    });

    const { loading: loadingTypes, nodes: types } = useQuery(
      stageGraph.assetTypeList
    );

    provide("mediaList", mediaList);
    provide("loading", loading);
    provide("refresh", refresh);
    provide("popNode", popNode);
    provide("types", types);

    return {
      fetch,
      loading,
      loadingTypes,
      types,
      filter,
      refresh,
      users,
      displayName,
      stageList,
      isGuest,
    };
  },
};
</script>

<style>
.type-name {
  text-transform: capitalize;
}
</style>