<template>
  <section class="hero is-small is-primary is-bold">
    <div class="hero-body">
      <h1 class="title">Stage Management</h1>
    </div>
  </section>
  <div class="columns">
    <div class="column is-narrow">
      <aside class="menu box has-background-light mx-4">
        <p class="menu-label">
          <span v-if="id">{{ stage.name }}</span>
          <span v-else>Create new stage</span>
        </p>
        <ul class="menu-list">
          <li>
            <router-link
              :to="
                id
                  ? `/dashboard/stage-management/${id}/`
                  : '/dashboard/new-stage'
              "
              exact-active-class="is-active"
              >General Information</router-link
            >
          </li>
          <template v-if="id">
            <li>
              <router-link to="layout" exact-active-class="is-active"
                >Layout</router-link
              >
            </li>
            <li id="media-menu">
              <router-link to="media" exact-active-class="is-active">
                Media
              </router-link>
            </li>
            <li>
              <router-link to="chat" exact-active-class="is-active">
                Chat
              </router-link>
            </li>
            <li>
              <router-link to="scenes" exact-active-class="is-active">
                Scenes
              </router-link>
            </li>
          </template>
        </ul>

        <p v-if="id" class="menu-label">
          <router-link
            :to="`/live/${stage.fileLocation}`"
            class="button is-block is-primary"
          >
            Enter!
          </router-link>
        </p>
      </aside>
    </div>
    <div class="column">
      <div class="pt-4 pr-4 pb-4">
        <Skeleton v-if="!!id && loading" />
        <router-view v-else />
      </div>
    </div>
  </div>
</template>

<script>
import { provide, watch } from "vue";
import { useFirst, useRequest } from "@/services/graphql/composable";
import { stageGraph } from "@/services/graphql";
import Skeleton from "@/components/Skeleton";
export default {
  props: ["id"],
  components: { Skeleton },
  setup: (props) => {
    const { nodes, loading, fetch } = useRequest(stageGraph.getStage);
    const stage = useFirst(nodes);
    provide("stage", stage);
    watch(
      () => props.id,
      () => {
        if (props.id) {
          fetch(props.id);
        }
      },
      { immediate: true }
    );
    return { stage, loading };
  },
};
</script>

<style>
</style>