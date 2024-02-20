<template>
  <section class="hero is-small is-primary is-bold">
    <div class="hero-body">
      <template v-if="id">
        <h1 class="title" v-if="stage.name">
          {{ stage.name }}
          <router-link
            :to="`/${stage.fileLocation}`"
            target="_blank"
            class="button is-light"
          >
            <span>{{ $t("enter") }}</span>
            <span class="icon">
              <i class="fas fa-chevron-right"></i>
            </span>
          </router-link>
        </h1>
        <p class="subtitle">{{ $t("stage_management") }}</p>
      </template>
      <h1 v-else class="title">{{ $t("create_new_stage") }}</h1>
    </div>
  </section>
  <div class="container-fluid">
    <div class="columns">
      <div class="column is-3 is-2-fullhd">
        <aside class="menu box has-background-light mx-4">
          <ul class="menu-list">
            <li>
              <router-link
                :to="
                  id
                    ? `/backstage/stage-management/${id}/`
                    : '/backstage/new-stage'
                "
                exact-active-class="is-active"
                >{{ $t("general_information") }}</router-link
              >
            </li>
            <template v-if="id">
              <li>
                <router-link
                  to="customisation"
                  exact-active-class="is-active"
                  >{{ $t("customisation") }}</router-link
                >
              </li>
              <li id="media-menu">
                <router-link to="media" exact-active-class="is-active">{{
                  $t("media")
                }}</router-link>
              </li>
              <li>
                <router-link to="archive" exact-active-class="is-active">{{
                  $t("archive")
                }}</router-link>
              </li>
            </template>
          </ul>
        </aside>
      </div>
      <div class="column is-9 is-10-fullhd">
        <div class="pt-4 pr-4 pb-4">
          <Loading v-if="!!id && loading" />
          <router-view v-else />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { provide, watch } from "vue";
import { useFirst, useRequest } from "@/services/graphql/composable";
import { stageGraph } from "@/services/graphql";
import Loading from "@/components/Loading";
export default {
  props: ["id"],
  components: { Loading },
  setup: (props) => {
    const { nodes, loading, fetch, data, refresh, clearCache } = useRequest(
      stageGraph.getStage,
    );
    const stage = useFirst(nodes);
    provide("stage", stage);
    provide("refresh", refresh);
    provide("clearCache", clearCache);
    watch(
      () => props.id,
      () => {
        if (props.id) {
          fetch(props.id);
        } else {
          data.value = null;
        }
      },
      { immediate: true },
    );
    return { stage, loading };
  },
};
</script>

<style></style>
