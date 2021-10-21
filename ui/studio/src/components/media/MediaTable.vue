<script lang="ts" setup>
import { ref } from '@vue/reactivity';
import { onMounted } from '@vue/runtime-core';
import { AssetTypeName, Media } from '../../models/media';
import { media } from '../../models/mock'
import { absolutePath } from '../../utils/common';

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

const data = ref<Media[]>([])
const loading = ref(false)
const fetchMedia = async () => {
  loading.value = true
  data.value = media.data.assetList.edges.filter(e => e.node.assetType.name !== AssetTypeName.Audio && e.node.assetType.name !== AssetTypeName.Stream).map(e => e.node)
  loading.value = false
}

const pagination = {
  showQuickJumper: true
}

onMounted(fetchMedia)

                                                                                                                                                                                                                                                        </script>

<template>
  <a-table
    class="mx-4 shadow rounded-md bg-white"
    :columns="columns"
    :data-source="data"
    rowKey="id"
    :loading="loading"
    :pagination="pagination"
  >
    <template #preview="{ record }">
      <a-image :src="absolutePath(record.src)" />
    </template>
    <template #date="{ text }">
      <d-date :value="text" />
    </template>
  </a-table>
</template>