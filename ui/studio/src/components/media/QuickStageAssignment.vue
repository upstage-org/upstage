<script setup lang="ts">
import { useQuery } from '@vue/apollo-composable';
import gql from 'graphql-tag';
import { computed, PropType, ref } from 'vue';
import { StudioGraph } from '../../models/studio';
import { Media } from '../../models/studio'
const props = defineProps({
  media: {
    type: Object as PropType<Media>,
    required: true,
  },
});

const visible = ref(false);
const keyword = ref('');

const { result, loading, refetch } = useQuery<StudioGraph>(gql`
{
  whoami {
    username
  }
  stages {
    edges {
      node {
        dbId
        name
        createdOn
        owner {
          username
          displayName
        }
      }
    }
  }
}`, null, {
  fetchPolicy: 'cache-only',
});

const dataSource = computed(() => {
  if (result.value) {
    const s = keyword.value.trim();
    return result.value.stages.edges.filter(({ node }) => {
      if (node.owner.username !== result.value?.whoami.username) {
        return false;
      }
      if (node.name.toLowerCase().includes(s)) {
        return true;
      }
      return false;
    }).map(({ node }) => node);
  }
  return []
})
</script>

<template>
  <a-button class="ml-2" type="primary" @click="visible = true">
    <plus-circle-outlined />Assign to stage
  </a-button>
  <a-drawer
    v-model:visible="visible"
    class="custom-class"
    style="color: red"
    title="Assign this media to one of your stages"
    placement="right"
    width="500"
  >
    <div class="flex">
      <a-input-search class="mr-2" placeholder="Stage name" v-model:value="keyword"></a-input-search>
    </div>
    <a-list
      class="demo-loadmore-list"
      :loading="loading"
      item-layout="horizontal"
      :data-source="dataSource"
    >
      <template #renderItem="{ item }">
        <a-list-item class="p-0">
          <template #actions>
            <a-tooltip
              v-if="media.stages.some(s => s.id === item.dbId)"
              title="Already assigned"
              placement="topRight"
            >
              <a-button disabled>
                <check-outlined />
              </a-button>
            </a-tooltip>
            <a-tooltip v-else :title="`Assign ${media.name} to this stage`" placement="topRight">
              <a-button type="primary">
                <plus-outlined />
              </a-button>
            </a-tooltip>
          </template>
          <a-list-item-meta>
            <template #title>
              <a-button
                type="text"
                class="p-0"
                style="position: relative; top: 8px;"
              >{{ item.name }}</a-button>
            </template>
            <template #description>
              <small style="position: relative; top: -4px;">
                Created by {{ item.owner.displayName || item.owner.username }}
                <d-date :value="item.createdOn"></d-date>
              </small>
            </template>
          </a-list-item-meta>
        </a-list-item>
      </template>
    </a-list>
  </a-drawer>
</template>