<script lang="ts" setup>
import { useMutation, useQuery } from '@vue/apollo-composable';
import { message } from 'ant-design-vue';
import gql from 'graphql-tag';
import { computed, reactive, watch, provide, ref, inject, Ref } from 'vue';
import { editingMediaVar, inquiryVar } from '../../apollo';
import configs from '../../config';
import { permissionFragment } from '../../models/fragment';
import { Media, MediaAttributes, StudioGraph, UploadFile } from '../../models/studio';
import { absolutePath } from '../../utils/common';
import MediaPreview from './MediaPreview.vue';
import RequestPermission from './MediaForm/RequestPermission.vue';
import RequestAcknowledge from './MediaForm/RequestAcknowledge.vue';

const files = inject<Ref<UploadFile[]>>("files")

const tableParams = reactive({
  limit: 10,
  cursor: undefined,
  sort: 'CREATED_ON_DESC',
})
const { result: inquiryResult } = useQuery(gql`{ inquiry @client }`)
const params = computed(() => ({
  ...tableParams,
  ...inquiryResult.value.inquiry
}))
watch(inquiryResult, () => {
  tableParams.cursor = undefined
})

const { result, loading, fetchMore } = useQuery<StudioGraph, { cursor?: string, limit: number, sort?: string[] }>(gql`
query MediaTable($cursor: String, $limit: Int, $sort: [AssetSortEnum], $name: String, $mediaTypes: [String], $owners: [String], $stages: [Int], $tags: [String], $createdBetween: [Date]) {
  media(after: $cursor, first: $limit, sort: $sort, nameLike: $name, mediaTypes: $mediaTypes, owners: $owners, stages: $stages, tags: $tags, createdBetween: $createdBetween) {
    totalCount
    edges {
      cursor
      node {
        id
        name
        src
        createdOn
        size
        description
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
          id
        }
        tags
        copyrightLevel
        permissions {
          ...permissionFragment
        }
        privilege
      }
    }
  }
}
${permissionFragment}
`, params.value, { notifyOnNetworkStatusChange: true })

const updateQuery = (previousResult: StudioGraph, { fetchMoreResult }: any) => {
  return fetchMoreResult ?? previousResult
}

watch(params, () => {
  fetchMore({
    variables: params.value,
    updateQuery
  })
})

const columns = [
  {
    title: "Preview",
    align: "center",
    width: 96,
    key: 'preview'
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
  },
  {
    title: "Copyright Level",
    dataIndex: "copyrightLevel",
    key: "copyrightLevel",
  },
  {
    title: "Stages",
    key: 'stages',
    dataIndex: 'stages',
    width: 250
  },
  {
    title: "Tags",
    key: 'tags',
    dataIndex: 'tags',
    width: 250
  },
  {
    title: "Size",
    dataIndex: "size",
    key: "size",
    sorter: {
      multiple: 4,
    },
  },
  {
    title: "Date",
    dataIndex: "createdOn",
    key: "created_on",
    sorter: {
      multiple: 5,
    },
    defaultSortOrder: 'descend'
  },
  {
    title: "Manage Media",
    align: "center",
    fixed: "right",
    key: 'actions'
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
  Object.assign(tableParams, {
    cursor: current > 1 ? window.btoa(`arrayconnection:${(current - 1) * pageSize}`) : undefined,
    limit: pageSize,
    sort
  })
}
const dataSource = computed(() => result.value ? result.value.media.edges.map((edge) => edge.node) : [])

const { loading: deleting, mutate: deleteMedia, onDone } = useMutation(gql`
mutation deleteMedia($id: ID!) {
  deleteMedia(id: $id) {
    success
    message
  }
}`)
onDone((result) => {
  console.log()
  if (result.data.deleteMedia.success) {
    message.success('Media deleted successfully')
  } else {
    message.error(result.data.deleteMedia.message)
  }
  fetchMore({
    variables: params.value,
    updateQuery
  })
})

provide('refresh', () => {
  fetchMore({
    variables: params.value,
    updateQuery
  })
})

const editMedia = (media: Media) => {
  editingMediaVar(media)
}

const composingMode = inject<Ref<boolean>>('composingMode')

const addFrameToEditingMedia = (media: Media) => {
  if (files && composingMode) {
    let frames = [media.src]
    const attribute = JSON.parse(media.description || '{}') as MediaAttributes
    if (attribute.multi) {
      frames = attribute.frames
    }
    files.value = files.value.concat(frames.map<UploadFile>((frame, i) => ({
      id: files.value.length + i,
      preview: absolutePath(frame),
      url: frame,
      status: 'uploaded',
      file: {
        name: frame,
      } as File
    })))
    composingMode.value = false
  }
}

const filterTag = (tag: string) => {
  inquiryVar({
    ...inquiryVar(),
    tags: [tag]
  })
}
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
    <template #bodyCell="{ column, record, text }">
      <template v-if="column.key === 'preview'">
        <MediaPreview :media="record" />
      </template>
      <template v-if="column.key === 'asset_type_id'">
        <span class="capitalize">{{ text }}</span>
      </template>
      <template v-if="column.key === 'owner_id'">
        <span v-if="text.displayName">
          <b>{{ text.displayName }}</b>
          <br />
          <span class="text-gray-500">{{ text.username }}</span>
        </span>
        <span v-else>
          <span>{{ text.username }}</span>
        </span>
      </template>
      <template v-if="column.key === 'stages'">
        <a v-for="(stage, i) in text" :key="i" :href="`${configs.UPSTAGE_URL}/${stage.url}`">
          <a-tag color="#007011">{{ stage.name }}</a-tag>
        </a>
      </template>
      <template v-if="column.key === 'tags'">
        <a-tag
          v-for="(tag, i) in text"
          :key="i"
          :color="tag"
          @click="filterTag(tag)"
          class="cursor-pointer"
        >{{ tag }}</a-tag>
      </template>
      <template v-if="column.key === 'size'">
        <a-tag v-if="text" :color="text < 100000 ? 'green' : text < 500000 ? 'gold' : 'red'">
          <d-size :value="text" />
        </a-tag>
        <a-tag v-else>No size</a-tag>
      </template>
      <template v-if="column.key === 'copyrightLevel'">
        <span
          class="leading-4"
        >{{ configs.MEDIA_COPYRIGHT_LEVELS.find(l => l.value === record.copyrightLevel)?.name }}</span>
      </template>
      <template v-if="column.key === 'created_on'">
        <d-date :value="text" />
      </template>
      <template v-if="column.key === 'actions'">
        <a-space v-if="composingMode">
          <a-button type="primary" @click="addFrameToEditingMedia(record)">
            <DoubleRightOutlined />Append frames
          </a-button>
        </a-space>
        <template v-else>
          <a-space v-if="record.privilege === 'NONE'">
            <a-tooltip>
              <template #title>You don't have permission to access this media</template>
              🙅‍♀️🙅‍♂️
            </a-tooltip>
          </a-space>
          <a-space v-else-if="record.privilege === 'REQUIRE_APPROVAL'">
            <RequestPermission v-if="record.copyrightLevel === 2" :media="record" />
            <RequestAcknowledge v-else :media="record" />
          </a-space>
          <a-space
            v-else-if="record.privilege === 'PENDING_APPROVAL'"
            direction="vertical"
            class="leading-4"
          >
            <b>✅ Request sent!</b>
            <small>Please wait for the media owner's approval</small>
          </a-space>
          <a-space v-else>
            <a-button type="primary" @click="editMedia(record)">
              <EditOutlined />Edit
            </a-button>
            <a :href="absolutePath(record.src)" :download="record.name">
              <a-button>
                <template #icon>
                  <DownloadOutlined />
                </template>
              </a-button>
            </a>
            <a-popconfirm
              title="Are you sure delete this media?"
              ok-text="Yes"
              cancel-text="No"
              @confirm="deleteMedia(record)"
              placement="left"
              :ok-button-props="{ danger: true }"
              loading="deleting"
            >
              <a-button type="dashed" danger>
                <template #icon>
                  <DeleteOutlined />
                </template>
              </a-button>
            </a-popconfirm>
          </a-space>
        </template>
      </template>
    </template>
  </a-table>
  <slot></slot>
</template>