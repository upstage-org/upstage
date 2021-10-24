<script lang="ts" setup>
import { ref, watch, inject, computed } from 'vue';
import Notifications from './Notifications.vue';
import { useQuery } from '@vue/apollo-composable';
import { useDebounceFn } from '@vueuse/core'
import gql from 'graphql-tag';
import { StudioGraph } from '../../models/studio';
import { inquiryVar } from '../../apollo';

const { result, loading } = useQuery<StudioGraph>(gql`
{
  users {
    edges {
      node {
        displayName
        username
      }
    }
  }
  stages {
    edges {
      node {
        dbId
        name
      }
    }
  }
  mediaTypes {
    edges {
      node {
        name
      }
    }
  }
}`)

const mode = ref<'simple' | 'advanced'>('advanced')
const name = ref('')
const owners = ref([])
const types = ref([])
const stages = ref([])

const updateInquiry = (vars: any) => inquiryVar({
  ...inquiryVar(),
  ...vars
})
watch(name, useDebounceFn(() => {
  updateInquiry({ name: name.value })
}, 500))
watch(owners, owners => {
  updateInquiry({ owners })
})
watch(stages, stages => {
  updateInquiry({ stages })
})
watch(types, mediaTypes => {
  updateInquiry({ mediaTypes })
})
const clearFilters = () => {
  name.value = ''
  owners.value = []
  types.value = []
  stages.value = []
}
const hasFilter = computed(() => name.value || owners.value.length || types.value.length || stages.value.length)
const handleFilterOwnerName = (keyword: string, option: any) => {
  const s = keyword.toLowerCase()
  return option.value.toLowerCase().includes(s) || option.label.toLowerCase().includes(s)
}
const handleFilterStageName = (keyword: string, option: any) => {
  return option.label.toLowerCase().includes(keyword.toLowerCase())
}

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
        <a-input-search allowClear class="w-48" placeholder="Search media" v-model:value="name" />
        <a-radio-group v-model:value="mode" button-style="solid">
          <a-radio-button value="simple">Simple</a-radio-button>
          <a-radio-button value="advanced">Advanced</a-radio-button>
        </a-radio-group>
        <template v-if="mode === 'advanced'">
          <a-select
            allowClear
            showArrow
            :filterOption="handleFilterOwnerName"
            mode="tags"
            style="min-width: 96px"
            placeholder="Owners"
            :loading="loading"
            v-model:value="owners"
            :options="result ? result.users.edges.map(e => ({ value: e.node.username, label: e.node.displayName || e.node.username })) : []"
          ></a-select>
          <a-select
            allowClear
            showArrow
            filterOption
            mode="tags"
            style="min-width: 128px"
            placeholder="Media types"
            :loading="loading"
            v-model:value="types"
            :options="result ? result.mediaTypes.edges.map(e => ({ value: e.node.name, label: e.node.name[0].toUpperCase() + e.node.name.substr(1) })) : []"
          ></a-select>
          <a-select
            allowClear
            showArrow
            :filterOption="handleFilterStageName"
            mode="tags"
            style="min-width: 160px"
            placeholder="Stages assigned"
            :loading="loading"
            v-model:value="stages"
            :options="result ? result.stages.edges.map(e => ({ value: e.node.dbId, label: e.node.name })) : []"
          ></a-select>
          <a-range-picker :placeholder="['Created from', 'to date']" />
          <a-button v-if="hasFilter" type="dashed" @click="clearFilters">
            <ClearOutlined />Clear Filters
          </a-button>
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