<script setup lang="ts">
import { useQuery } from '@vue/apollo-composable';
import gql from 'graphql-tag';
import { ref, computed } from 'vue';
import { Stage, StudioGraph } from '../../../models/studio';


const { result, loading } = useQuery<StudioGraph>(gql`
{
  stages {
    edges {
      node {
        dbId
        name
      }
    }
  }
}
`, null, { fetchPolicy: "cache-only" })
const stages = computed(() => {
  if (result.value?.stages) {
    return result.value.stages.edges.map(({ node }) => node).map(({ dbId, name }) => ({ key: dbId, name }));
  }
  return []
})


const targetKeys = ref<string[]>([]);
const filterOption = (inputValue: string, option: Stage) => {
  return option.name.toLowerCase().indexOf(inputValue.toLowerCase()) > -1;
};
const handleChange = (keys: string[], direction: string, moveKeys: string[]) => {
  console.log(keys, direction, moveKeys);
};

const handleSearch = (dir: string, value: string) => {
  console.log('search:', dir, value);
};
</script>

<template>
  <a-transfer
    :locale="{
      itemUnit: 'stage',
      itemsUnit: 'stages',
      notFoundContent: 'No stage available',
      searchPlaceholder: 'Search stage name'
    }"
    :list-style="{
      flex: '1'
    }"
    :titles="[' available', ' assigned']"
    v-model:target-keys="targetKeys"
    :data-source="stages"
    show-search
    :filter-option="filterOption"
    :render="(item: Stage) => item.name"
    @change="handleChange"
    @search="handleSearch"
  />
</template>