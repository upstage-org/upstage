<script lang="ts" setup>
import { useQuery } from '@vue/apollo-composable';
import gql from 'graphql-tag';
import { computed, watch } from 'vue';
import { StudioGraph } from '../../models/studio';
import { absolutePath } from '../../utils/common';

const { result, loading, fetchMore } = useQuery<StudioGraph, { cursor?: string, limit: number, sort?: string }>(gql`
query MediaTable($page: Int, $size: Int, $sort: [AssetSortEnum]) {
  media(page: $page, size: $size, sort: $sort) {
    totalCount
    edges {
      cursor
      node {
        id
        name
        src
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
    sorter: true
  },
  {
    title: "Type",
    dataIndex: 'assetType.name'
  },
  {
    title: "Owner",
    dataIndex: 'owner.username'
  },
  {
    title: "Stage",
    slot: "stage",
  },
  {
    title: "Date",
    type: "date",
    dataIndex: "createdOn",
    slots: { customRender: 'date' },
  },
  {
    title: "Manage Media",
    slot: "manage",
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
  column: object
  columnKey: string
  field: string
  order: "ascend" | "descend"
}

const handleTableChange = ({ current, pageSize }: Pagination, _: any, { columnKey, order }: Sorter) => {
  fetchMore({
    variables: {
      cursor: window.btoa(`arrayconnection:${(current - 1) * pageSize}`),
      limit: pageSize,
      sort: `${columnKey}_${order === 'ascend' ? 'ASC' : 'DESC'}`.toUpperCase()
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
      <a-image :src="absolutePath(record.src)" />
    </template>
    <template #date="{ text }">
      <d-date :value="text" />
    </template>
  </a-table>
</template>