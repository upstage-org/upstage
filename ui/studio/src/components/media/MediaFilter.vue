<script lang="ts" setup>
import { ref, watch, inject } from 'vue';
import Notifications from './Notifications.vue';
import { useQuery } from '@vue/apollo-composable';
import gql from 'graphql-tag';
import { StudioGraph } from '../../models/studio';

const { result, loading } = useQuery<StudioGraph>(gql`
{
  users {
    edges {
      node {
        id
        displayName
        username
      }
    }
  }
  stages {
    edges {
      node {
        id
        name
      }
    }
  }
  mediaTypes {
    edges {
      node {
        id
        name
      }
    }
  }
}`)
watch(result, console.log)

const mode = ref<'simple' | 'advanced'>('advanced')
const owners = ref([])
const types = ref([])
const stages = ref([])
const visibleDropzone = inject('visibleDropzone')
</script>

<template>
  <a-affix :offset-top="0">
    <a-space
      class="shadow rounded-md m-4 px-4 py-2 bg-gradient-to-r from-gray-800 to-white flex justify-between"
    >
      <a-space class="flex-wrap">
        <a-button type="primary" @click="visibleDropzone = true">
          <template #icon>
            <PlusOutlined />
          </template>
          New
        </a-button>
        <a-input-search class="w-48" placeholder="Search media" />
        <a-radio-group v-model:value="mode" button-style="solid">
          <a-radio-button value="simple">Simple</a-radio-button>
          <a-radio-button value="advanced">Advanced</a-radio-button>
        </a-radio-group>
        <template v-if="mode === 'advanced'">
          <a-select
            showArrow
            mode="tags"
            style="min-width: 96px"
            placeholder="Owners"
            :loading="loading"
            v-model:value="owners"
            :options="result ? result.users.edges.map(e => ({ value: e.node.id, label: e.node.displayName || e.node.username })) : []"
          ></a-select>
          <a-select
            showArrow
            mode="tags"
            style="min-width: 128px"
            placeholder="Media types"
            :loading="loading"
            v-model:value="types"
            :options="result ? result.mediaTypes.edges.map(e => ({ value: e.node.id, label: e.node.name })) : []"
          ></a-select>
          <a-select
            showArrow
            mode="tags"
            style="min-width: 160px"
            placeholder="Stages assigned"
            :loading="loading"
            v-model:value="stages"
            :options="result ? result.stages.edges.map(e => ({ value: e.node.id, label: e.node.name })) : []"
          ></a-select>
          <a-range-picker :placeholder="['Created from', 'to date']" />
        </template>
      </a-space>
      <a-space>
        <div style="line-height: 0.8;" class="text-right">
          <h2 class="mb-0">Helen</h2>
          <span class="text-gray-500">Admin</span>
        </div>
        <Notifications />
        <a-dropdown class="ml-4">
          <a class="ant-dropdown-link flex-nowrap block w-24" @click.prevent>
            <img src="../../assets/upstage.png" class="h-6" />
            <DownOutlined />
          </a>
          <template #overlay>
            <a-menu>
              <a-menu-item>Back to Backstage</a-menu-item>
              <a-menu-item>Logout</a-menu-item>
            </a-menu>
          </template>
        </a-dropdown>
      </a-space>
    </a-space>
  </a-affix>
</template>