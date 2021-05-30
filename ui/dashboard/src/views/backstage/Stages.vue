<template>
  <section class="hero is-small is-primary is-bold">
    <div class="hero-body">
      <Breadcrumb
        description="Create a new stage, enter or manage an existing stage"
      />
      <h1 class="title is-inline">Stages</h1>
      &nbsp;
      <router-link to="/backstage/new-stage" class="button">
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
        Pres <strong>New</strong> button to create a new future stage. Click
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
import { useOwners, useQuery } from "@/services/graphql/composable";
import { stageGraph } from "@/services/graphql";
import Skeleton from "@/components/Skeleton.vue";
import { includesIgnoreCase } from "@/utils/common";
import { useStore } from "vuex";
import { displayName } from "@/utils/auth";
import Breadcrumb from "@/components/Breadcrumb";

export default {
  components: { StageTable, Field, Switch, Dropdown, Skeleton, Breadcrumb },
  setup: () => {
    const store = useStore();
    const currentUser = computed(() => store.state.user.user);
    const filter = reactive({
      mine: true,
      keyword: "",
    });

    const { loading, nodes, refresh } = useQuery(stageGraph.stageList);
    provide("refresh", refresh);

    const owners = useOwners(nodes);

    const stageList = computed(() => {
      let result = nodes.value;
      if (filter.keyword) {
        result = result.filter((stage) =>
          includesIgnoreCase(stage.name, filter.keyword)
        );
      }
      if (filter.mine) {
        result = result.filter(
          (stage) => stage.owner.id === currentUser.value.id
        );
        return result;
      }
      if (filter.owner) {
        result = result.filter((stage) => stage.owner.id === filter.owner);
      }
      return result;
    });

    return { filter, loading, stageList, owners, displayName };
  },
};
</script>

<style lang="scss" scoped>
</style>