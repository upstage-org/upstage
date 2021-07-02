<template>
  <section class="hero is-small is-primary is-bold">
    <div class="hero-body">
      <template v-if="id">
        <h1 class="title" v-if="stage.name">
          {{ stage.name }}
          <router-link
            :to="`/live/${stage.fileLocation}`"
            class="button is-light"
          >
            <span>ENTER</span>
            <span class="icon">
              <i class="fas fa-chevron-right"></i>
            </span>
          </router-link>
        </h1>
        <p class="subtitle">Stage Management</p>
      </template>
      <h1 v-else class="title">Create new stage</h1>
    </div>
  </section>
  <div class="container-fluid">
    <div class="columns">
      <div class="column is-narrow">
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
                >General Information</router-link
              >
            </li>
            <template v-if="id">
              <li>
                <router-link to="customization" exact-active-class="is-active"
                  >Customization</router-link
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
                <router-link to="records" exact-active-class="is-active">
                  Records
                </router-link>
              </li>
              <li>
                <router-link to="scenes" exact-active-class="is-active">
                  Scenes
                </router-link>
              </li>
            </template>
          </ul>
        </aside>
      </div>
      <div class="column">
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
    const { nodes, loading, fetch, data, refresh } = useRequest(
      stageGraph.getStage
    );
    const stage = useFirst(nodes);
    provide("stage", stage);
    provide("refresh", refresh);
    watch(
      () => props.id,
      () => {
        if (props.id) {
          fetch(props.id);
        } else {
          data.value = null;
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