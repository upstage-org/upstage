<template>
  <section class="hero is-small is-primary is-bold">
    <div class="hero-body">
      <h1 class="title">Stage Management</h1>
    </div>
  </section>
  <div class="columns">
    <div class="column is-4">
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
            <li>
              <router-link to="chat" exact-active-class="is-active"
                >Chat</router-link
              >
            </li>
            <li><a>Record</a></li>
            <li>
              <router-link to="scenes" exact-active-class="is-active"
                >Scenes</router-link
              >
              <ul>
                <li><a>Avatar</a></li>
                <li><a>Props</a></li>
                <li><a>Backdrop</a></li>
                <li><a>Sound</a></li>
                <li><a>Videos</a></li>
                <li><a>Loading</a></li>
              </ul>
            </li>
          </template>
        </ul>
      </aside>
    </div>
    <div class="column is-8">
      <div class="pt-4 pr-4 pb-4">
        <Skeleton v-if="!!id && loading" height="400px" />
        <router-view v-else />
      </div>
    </div>
  </div>
</template>

<script>
import { computed, provide, watch } from "vue";
import { useFirst, useRequest } from "@/services/graphql/composable";
import { stageGraph } from "@/services/graphql";
import Skeleton from "@/components/Skeleton";
export default {
  props: ["id"],
  components: { Skeleton },
  setup: (props) => {
    provide(
      "id",
      computed(() => props.id)
    );
    const { nodes, loading, fetch } = useRequest(stageGraph.stageList);
    const stage = useFirst(nodes);
    provide("stage", stage);
    watch(
      () => props.id,
      () => {
        if (props.id) {
          fetch({
            id: props.id,
          });
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