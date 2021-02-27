<template>
  <section class="section">
    <div class="container">
      <h1 class="title">
        My Stages
        <button class="button mx-2 is-dark">
          <span>New</span>
          <span class="icon">
            <i class="fa fa-plus"></i>
          </span>
        </button>
        <button class="button mx-2 is-dark">
          <span>Search</span>
          <span class="icon">
            <i class="fa fa-search"></i>
          </span>
        </button>
      </h1>
      <div class="columns">
        <div class="column is-3" v-for="stage in stages" :key="stage">
          <Stage :stage="stage" />
        </div>
      </div>
    </div>
  </section>
  <section class="section">
    <div class="container">
      <h1 class="title">Other Stages</h1>
      <div class="columns">
        <div class="column is-3" v-for="stage in stages" :key="stage">
          <Stage :stage="stage" />
        </div>
      </div>
    </div>
  </section>
  I
</template>

<script>
import Stage from "@/components/stage/Stage";
import { useQuery } from "@/services/graphql/composable";
import { stageGraph } from "@/services/graphql";
export default {
  components: { Stage },
  setup: () => {
    const { nodes: stages, loading } = useQuery(stageGraph.stageList);
    return { loading, stages };
  },
};
</script>

<style>
</style>