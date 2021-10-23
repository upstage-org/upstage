<script lang="ts" setup>
import { useQuery } from '@vue/apollo-composable';
import gql from 'graphql-tag';
import { computed, watch } from 'vue';
import configs from '../../config';
import { StudioGraph } from '../../models/studio';
import { absolutePath } from '../../utils/common';

const { result, loading, fetchMore } = useQuery<StudioGraph, { cursor?: string, limit: number, sort?: string[] }>(gql`
query MediaTable($cursor: String, $limit: Int, $sort: [AssetSortEnum]) {
  media(after: $cursor, first: $limit, sort: $sort) {
    totalCount
    edges {
      cursor
      node {
        id
        name
        src
        createdOn
        assetType {
          name
        }
        owner {
          username
          displayName
        }
        stages {
          name
          url
        }
      }
    }
  }
}
`, { limit: 10 }, { notifyOnNetworkStatusChange: true })

const columns = [
  {
    title: "Preview",
    align: "center",
    width: 96,
    slots: { customRender: 'preview' },
  },
  {
    title: "Name",
    dataIndex: "name",
    key: "name",
    sorter: {
      multiple: 3,
    },
  },
  {
    title: "Type",
    dataIndex: ['assetType', 'name'],
    key: 'asset_type_id',
    slots: { customRender: 'type' },
    sorter: {
      multiple: 1,
    },
  },
  {
    title: "Owner",
    dataIndex: 'owner',
    key: 'owner_id',
    sorter: {
      multiple: 2,
    },
    slots: { customRender: 'owner' },
  },
  {
    title: "Stages",
    key: 'stages',
    dataIndex: 'stages',
    slots: { customRender: 'stages' },
  },
  {
    title: "Date",
    type: "date",
    dataIndex: "createdOn",
    key: "created_on",
    slots: { customRender: 'date' },
    sorter: {
      multiple: 4,
    },
    defaultSortOrder: 'descend'
  },
  {
    title: "Manage Media",
    align: "center",
    fixed: "right",
    slots: { customRender: 'actions' },
  },
];

interface Pagination {
  current: number
  pageSize: number
  showQuickJumper: boolean
  showSizeChanger: boolean
  total: number
}

interface Sorter {
  column: any
  columnKey: string
  field: string
  order: "ascend" | "descend"
}

const handleTableChange = ({ current, pageSize }: Pagination, _: any, sorter: Sorter | Sorter[]) => {
  const sort = (Array.isArray(sorter) ? sorter : [sorter])
    .sort((a, b) => a.column.sorter.multiple - b.column.sorter.multiple)
    .map(({ columnKey, order }) => `${columnKey}_${order === 'ascend' ? 'ASC' : 'DESC'}`.toUpperCase())
  fetchMore({
    variables: {
      cursor: window.btoa(`arrayconnection:${(current - 1) * pageSize}`),
      limit: pageSize,
      sort
    },
    updateQuery: (previousResult, { fetchMoreResult }) => {
      if (!fetchMoreResult) return previousResult
      return fetchMoreResult
    },
  })
}
const dataSource = computed(() => result.value ? result.value.media.edges.map((edge) => edge.node) : [])
</script>

<template>
  <a-table
    class="mx-4 shadow rounded-md bg-white"
    :columns="columns"
    :data-source="dataSource"
    rowKey="id"
    :loading="loading"
    @change="handleTableChange"
    :pagination="{
      showQuickJumper: true,
      showSizeChanger: true,
      total: result ? result.media.totalCount : 0,
    } as Pagination"
  >
    <template #preview="{ record }">
      <audio v-if="record.assetType.name === 'audio'" controls>
        <source :src="absolutePath(record.src)" />Your browser does not support the audio element.
      </audio>
      <video v-else-if="record.assetType.name === 'stream'" width="320" height="240" controls>
        <source :src="absolutePath(record.src)" />Your browser does not support the video tag.
      </video>
      <a-image v-else :src="absolutePath(record.src)" />
    </template>
    <template #type="{ text }">
      <span class="capitalize">{{ text }}</span>
    </template>
    <template #owner="{ text }">
      <span v-if="text.displayName">
        <b>{{ text.displayName }}</b>
        <br />
        <span class="text-gray-500">{{ text.username }}</span>
      </span>
      <span v-else>
        <span>{{ text.username }}</span>
      </span>
    </template>
    <template #stages="{ text: stages }">
      <a v-for="(stage,i) in stages" :href="`${configs.UPSTAGE_URL}/${stage.url}`">
        {{ stage.name }}
        <br />
      </a>
    </template>
    <template #date="{ text }">
      <d-date :value="text" />
    </template>
    <template #actions="{ text }">
      <a-button danger>
        <DeleteOutlined />Delete
      </a-button>
    </template>
  </a-table>
</template>