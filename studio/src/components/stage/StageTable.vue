<script lang="ts" setup>
import { useQuery } from "@vue/apollo-composable";
import gql from "graphql-tag";
import { computed, reactive, watch, provide, ref, inject, Ref } from "vue";
import { Media, Stage, StudioGraph } from "models/studio";
import { absolutePath } from "utils/common";
import { ColumnType, TablePaginationConfig } from "ant-design-vue/lib/table";
import { SorterResult } from "ant-design-vue/lib/table/interface";
import { useI18n } from "vue-i18n";
import { capitalize } from "utils/common";
import { IframeSrc } from "../../symbols";

const { t } = useI18n();

const iframeSrc = inject(IframeSrc, ref(""));
const manageStage = (stage: Stage) =>
  (iframeSrc.value = `/backstage/stage-management/${stage.id}/`);
const enterStage = (stage: Stage) => {
  window.open(`/${stage.fileLocation}`, "_blank");
};
const tableParams = reactive({
  limit: 10,
  cursor: undefined,
  sort: "CREATED_ON_DESC",
});
const { result: inquiryResult } = useQuery(
  gql`
    {
      inquiry @client
    }
  `
);
const params = computed(() => ({
  ...tableParams,
  ...inquiryResult.value.inquiry,
}));
watch(inquiryResult, () => {
  tableParams.cursor = undefined;
});

const { result, loading, fetchMore } = useQuery<
  StudioGraph,
  { cursor?: string; limit: number; sort?: string[] }
>(
  gql`
    query StageTable(
      $cursor: String
      $limit: Int
      $sort: [StageSortEnum]
      $name: String
      $owners: [String]
      $createdBetween: [Date]
    ) {
      stages(
        after: $cursor
        first: $limit
        sort: $sort
        nameLike: $name
        owners: $owners
        createdBetween: $createdBetween
      ) {
        totalCount
        edges {
          cursor
          node {
            id
            name
            cover
            createdOn
            lastAccess
            description
            permission
            visibility
            status
            fileLocation
            owner {
              username
              displayName
            }
          }
        }
      }
    }
  `,
  params.value,
  { notifyOnNetworkStatusChange: true }
);

const updateQuery = (previousResult: StudioGraph, { fetchMoreResult }: any) => {
  return fetchMoreResult ?? previousResult;
};

watch(params, () => {
  iframeSrc.value = "";
  fetchMore({
    variables: params.value,
    updateQuery,
  });
});

const columns: ColumnType<Stage>[] = [
  {
    title: t("preview"),
    align: "center",
    width: 96,
    key: "cover",
    dataIndex: "cover",
  },
  {
    title: t("name"),
    dataIndex: "name",
    key: "name",
    sorter: {
      multiple: 3,
    },
  },
  {
    title: t("owner"),
    dataIndex: "owner",
    key: "owner_id",
    sorter: {
      multiple: 2,
    },
  },
  {
    title: t("date"),
    dataIndex: "createdOn",
    key: "created_on",
    sorter: {
      multiple: 5,
    },
    defaultSortOrder: "descend",
  },
  {
    title: t("last_access"),
    dataIndex: "lastAccess",
    key: "last_access",
    sorter: {
      multiple: 6,
    },
    defaultSortOrder: "descend",
  },
  //    {
  //        title: t("recorded"),
  //        align: "center",
  //        key: "recording",
  //    },
  {
    title: t("status"),
    dataIndex: "status",
    key: "status",
  },
  {
    title: t("visibility"),
    dataIndex: "visibility",
    key: "visibility",
  },
  {
    title: t("access"),
    dataIndex: "permission",
    key: "permission",
  },
  {
    title: `${t("manage")} ${t("stage")}`,
    align: "center",
    fixed: "right",
    key: "actions",
  },
];

interface Pagination {
  current: number;
  pageSize: number;
  showQuickJumper: boolean;
  showSizeChanger: boolean;
  total: number;
}

interface Sorter {
  column: any;
  columnKey: string;
  field: string;
  order: "ascend" | "descend";
}

const handleTableChange = (
  { current = 1, pageSize = 10 }: TablePaginationConfig,
  _: any,
  sorter: SorterResult<Media> | SorterResult<Media>[]
) => {
  const sort = (Array.isArray(sorter) ? sorter : [sorter])
    .sort(
      (a, b) =>
        (a.column?.sorter as any).multiple - (b.column?.sorter as any).multiple
    )
    .map(({ columnKey, order }) =>
      `${columnKey}_${order === "ascend" ? "ASC" : "DESC"}`.toUpperCase()
    );
  Object.assign(tableParams, {
    cursor:
      current > 1
        ? window.btoa(`arrayconnection:${(current - 1) * pageSize}`)
        : undefined,
    limit: pageSize,
    sort,
  });
};
const dataSource = computed(() =>
  result.value ? result.value.stages.edges.map((edge) => edge.node) : []
);

provide("refresh", () => {
  fetchMore({
    variables: params.value,
    updateQuery,
  });
});
</script>

<template>
  <a-layout class="w-full">
    <a-table
      class="w-full shadow rounded-xl bg-white overflow-auto"
      :columns="columns"
      :data-source="dataSource"
      rowKey="id"
      :loading="loading"
      @change="handleTableChange"
      :pagination="{
        showQuickJumper: true,
        showSizeChanger: true,
        total: result ? result.stages.totalCount : 0,
      } as Pagination"
    >
      <template #bodyCell="{ column, record, text }">
        <template v-if="column.key === 'cover'">
          <a-image
            :src="absolutePath(text)"
            class="w-24 max-h-24 object-contain"
          />
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
        <template v-if="['created_on', 'last_access'].includes(column.key)">
          <d-date v-if="text" :value="text" />
        </template>
        <template v-if="column.key === 'permission'">
          {{ capitalize(text) }}
        </template>
        <template v-if="column.key === 'status'">
          <a-tag
            v-if="text"
            :color="{ live: 'red', rehearsal: 'yellow', upcoming: 'green' }[(record as Stage).status]
            "
          >
            {{ capitalize(text) }}
          </a-tag>
        </template>
        <template v-if="column.key === 'visibility'">
          <a-switch :checked="text" disabled />
        </template>
        <template v-if="column.key === 'actions'">
          <a-space>
            <a-button @click="manageStage(record)">
              <setting-outlined />
              Manage
            </a-button>
            <a-button type="primary" @click="enterStage(record)">
              <login-outlined />
              Enter
            </a-button>
          </a-space>
        </template>
      </template>
    </a-table>
    <slot></slot>
  </a-layout>
</template>
