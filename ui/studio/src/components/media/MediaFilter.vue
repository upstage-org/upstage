<script lang="ts" setup>
import { ref } from '@vue/reactivity';
import { useStudioStore } from '../../store';
import Notifications from './Notifications.vue';

const mode = ref<'simple' | 'advanced'>('simple')
const value = ref([])
const handleChange = (value: string) => {
  console.log(`selected ${value}`);
};
const options = [...Array(25)].map((_, i) => ({ value: (i + 10).toString(36) + (i + 1) }))

const store = useStudioStore()

</script>

<template>
  <a-affix :offset-top="0">
    <a-space class="shadow rounded-md m-4 px-4 py-2 bg-white flex justify-between">
      <a-space class="flex-wrap">
        <a-button type="primary" @click="store.commit('INCREASE')">
          <template #icon>
            <PlusOutlined />
          </template>
          New {{ store.state.count }}
        </a-button>
        <a-input-search class="w-48" placeholder="Search media" />
        <a-radio-group v-model:value="mode" button-style="solid">
          <a-radio-button value="simple">Simple</a-radio-button>
          <a-radio-button value="advanced">Advanced</a-radio-button>
        </a-radio-group>
        <template v-if="mode === 'advanced'">
          <a-select
            v-model:value="value"
            mode="tags"
            style="min-width: 96px"
            placeholder="Owners"
            :options="options"
            @change="handleChange"
            showArrow
          ></a-select>
          <a-select
            v-model:value="value"
            mode="tags"
            style="min-width: 128px"
            placeholder="Media types"
            :options="options"
            @change="handleChange"
            showArrow
          ></a-select>
          <a-select
            v-model:value="value"
            mode="tags"
            style="min-width: 160px"
            placeholder="Stages assigned"
            :options="options"
            @change="handleChange"
            showArrow
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