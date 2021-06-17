<template>
  <section class="hero is-small is-primary is-bold">
    <div class="hero-body">
      <Breadcrumb
        description="Create a new stage, enter or manage an existing stage"
      />
      <h1 class="title is-inline">Stages</h1>
      &nbsp;
      <router-link v-if="!isGuest" to="/backstage/new-stage" class="button">
        <span>New</span>
        <span class="icon">
          <i class="fa fa-plus"></i>
        </span>
      </router-link>
    </div>
  </section>
  <section class="section">
    <div class="container">
      <h1 class="title">
        Stages
        <Switch
          v-model="filter.mine"
          :label="
            filter.mine ? 'Show my stages only' : 'Show stages created by: '
          "
        />
        <Dropdown
          v-if="!filter.mine"
          class="ml-2"
          v-model="filter.owner"
          :data="owners.concat({ displayName: 'All players' })"
          :render-value="(item) => item.id"
          :render-label="displayName"
          placeholder="Stage owner"
        />
        <Field
          class="ml-2"
          style="width: 200px; display: inline-block; vertical-align: top"
          v-model="filter.keyword"
          right="fas fa-search"
          placeholder="Stage name"
        />
      </h1>
      <h2 class="subtitle">
        Click <strong>New</strong> button to create a new future stage. Click
        <strong>Search</strong> button for search form to find Stage
      </h2>
      <Skeleton v-if="loading" />
      <StageTable v-else :data="stageList" />
    </div>
  </section>
</template>

<script>
import { reactive } from "@vue/reactivity";
import StageTable from "@/components/stage/StageTable";
import Field from "@/components/form/Field";
import Dropdown from "@/components/form/Dropdown";
import Switch from "@/components/form/Switch";
import { computed, provide } from "@vue/runtime-core";
import { useOwners } from "@/services/graphql/composable";
import Skeleton from "@/components/Skeleton.vue";
import { includesIgnoreCase } from "@/utils/common";
import { displayName } from "@/utils/auth";
import Breadcrumb from "@/components/Breadcrumb";
import { useStore } from "vuex";

export default {
  components: { StageTable, Field, Switch, Dropdown, Skeleton, Breadcrumb },
  setup: () => {
    const store = useStore();
    const isGuest = computed(() => store.getters["user/isGuest"]);

    const filter = reactive({
      mine: true,
      keyword: "",
    });

    const stages = computed(() => store.state.cache.stageList);
    const loading = computed(() => store.getters["cache/loadingStages"]);
    const refresh = () => store.dispatch("cache/fetchStages");
    provide("refresh", refresh);

    const owners = useOwners(stages);

    const stageList = computed(() => {
      if (loading.value) {
        return [];
      }
      let result = stages.value;
      if (filter.keyword) {
        result = result.filter((stage) =>
          includesIgnoreCase(stage.name, filter.keyword)
        );
      }
      if (filter.mine) {
        result = result.filter((stage) =>
          ["player", "editor", "owner"].includes(stage.permission)
        );
        return result;
      }
      if (filter.owner) {
        result = result.filter((stage) => stage.owner.id === filter.owner);
      }
      return result;
    });

    return { filter, loading, stageList, owners, displayName, isGuest };
  },
};
</script>

<style lang="scss" scoped>
</style>