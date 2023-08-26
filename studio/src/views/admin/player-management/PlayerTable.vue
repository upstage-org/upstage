<script lang="ts">
import { useMutation, useQuery } from "@vue/apollo-composable";
import gql from "graphql-tag";
import { computed, reactive, watch, provide, ref, inject, Ref } from "vue";
import type { Media, Stage, StudioGraph } from "models/studio";
import { absolutePath } from "utils/common";
import { ColumnType, TablePaginationConfig } from "ant-design-vue/lib/table";
import { SorterResult } from "ant-design-vue/lib/table/interface";
import { useI18n } from "vue-i18n";
import { capitalize } from "utils/common";
import { IframeSrc } from "symbols";
import { Layout, Table, message } from "ant-design-vue";
import { FetchResult } from "@apollo/client/core";
import { h } from "vue";

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

export default {
  setup(props, ctx) {
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
    const { result: inquiryResult } = useQuery(gql`
      {
        inquiry @client
      }
    `);
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
      { notifyOnNetworkStatusChange: true },
    );

    const updateQuery = (
      previousResult: StudioGraph,
      { fetchMoreResult }: any,
    ) => {
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
        align: "center",
      },
      {
        title: t("visibility"),
        dataIndex: "visibility",
        key: "visibility",
        align: "center",
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

    const handleTableChange = (
      { current = 1, pageSize = 10 }: TablePaginationConfig,
      _: any,
      sorter: SorterResult<Media> | SorterResult<Media>[],
    ) => {
      const sort = (Array.isArray(sorter) ? sorter : [sorter])
        .sort(
          (a, b) =>
            (a.column?.sorter as any).multiple -
            (b.column?.sorter as any).multiple,
        )
        .map(({ columnKey, order }) =>
          `${columnKey}_${order === "ascend" ? "ASC" : "DESC"}`.toUpperCase(),
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
      result.value ? result.value.stages.edges.map((edge) => edge.node) : [],
    );

    provide("refresh", () => {
      fetchMore({
        variables: params.value,
        updateQuery,
      });
    });

    const {
      mutate: updateStatus,
      loading: loadingUpdateStatus,
      onDone: onStatusUpdated,
    } = useMutation<{ updateStatus: { result: string } }, { stageId: string }>(
      gql`
        mutation UpdateStatus($stageId: ID!) {
          updateStatus(stageId: $stageId) {
            result
          }
        }
      `,
    );
    const handleChangeStatus = async (record: Stage) => {
      await updateStatus({
        stageId: record.id,
      });
    };

    const {
      mutate: updateVisibility,
      loading: loadingUpdateVisibility,
      onDone: onVisibilityUpdated,
    } = useMutation<
      { updateVisibility: { result: string } },
      { stageId: string }
    >(gql`
      mutation UpdateVisibility($stageId: ID!) {
        updateVisibility(stageId: $stageId) {
          result
        }
      }
    `);
    const handleChangeVisibility = async (record: Stage) => {
      await updateVisibility({
        stageId: record.id,
      });
    };

    const handleUpdate = (result: FetchResult) => {
      if (result.data) {
        message.success("Stage updated successfully!");
      } else {
        message.error("You don't have permission to perform this action!");
      }
      fetchMore({
        variables: params.value,
        updateQuery,
      });
    };

    onStatusUpdated(handleUpdate);
    onVisibilityUpdated(handleUpdate);

    return () =>
      h(
        Layout,
        {
          class: "w-full",
        },
        [
          h(Table, {
            class: "w-full shadow rounded-xl bg-white overflow-auto",
            rowKey: "id",
            columns,
            dataSource: dataSource.value,
            loading: loading.value,
            onChange: handleTableChange,
            pagination: {
              showQuickJumper: true,
              showSizeChanger: true,
              total: result.value ? result.value.stages.totalCount : 0,
            } as Pagination,
          }),
        ],
      );
  },
};
</script>
