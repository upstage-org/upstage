<script lang="ts">
import { useMutation, useQuery } from "@vue/apollo-composable";
import gql from "graphql-tag";
import { computed, reactive, watch, provide, ref, inject, Ref } from "vue";
import type { AdminPlayer, Media, Stage, StudioGraph } from "models/studio";
import { absolutePath, displayName } from "utils/common";
import { ColumnType, TablePaginationConfig } from "ant-design-vue/lib/table";
import { SorterResult } from "ant-design-vue/lib/table/interface";
import { useI18n } from "vue-i18n";
import { capitalize } from "utils/common";
import { IframeSrc } from "symbols";
import {
  Button,
  Layout,
  Popconfirm,
  Space,
  Spin,
  Switch,
  Table,
  Tooltip,
  message,
} from "ant-design-vue";
import { FetchResult } from "@apollo/client/core";
import { h } from "vue";
import DDate from "components/display/DDate.vue";
import DSize from "components/display/DSize.vue";
import {
  DeleteOutlined,
  EditOutlined,
  KeyOutlined,
} from "@ant-design/icons-vue";

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
        query AdminPlayerTable(
          $cursor: String
          $limit: Int
          $sort: [AdminPlayerSortEnum]
          $name: String
          $createdBetween: [Date]
        ) {
          adminPlayers(
            after: $cursor
            first: $limit
            sort: $sort
            usernameLike: $name
            createdBetween: $createdBetween
          ) {
            totalCount
            edges {
              cursor
              node {
                id
                active
                username
                email
                binName
                role
                roleName
                firstName
                lastName
                displayName
                createdOn
                uploadLimit
                intro
                dbId
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

    const columns: ColumnType<AdminPlayer>[] = [
      {
        title: t("username"),
        key: "username",
        dataIndex: "username",
        sorter: {
          multiple: 3,
        },
      },
      {
        title: t("display_name"),
        dataIndex: "username",
        customRender(opt) {
          return displayName(opt.record);
        },
        key: "display_name",
      },
      {
        title: t("email"),
        key: "email",
        dataIndex: "email",
        sorter: {
          multiple: 4,
        },
      },
      {
        title: t("date_registered"),
        dataIndex: "createdOn",
        key: "created_on",
        sorter: {
          multiple: 5,
        },
        defaultSortOrder: "descend",
        customRender(opt) {
          return h(DDate, {
            value: opt.text,
          });
        },
      },
      {
        title: t("last_access"),
        dataIndex: "lastAccess",
        key: "last_access",
        defaultSortOrder: "descend",
      },
      {
        title: t("role"),
        dataIndex: "roleName",
        key: "role",
        align: "center",
        sorter: {
          multiple: 1,
        },
      },
      {
        title: t("status"),
        dataIndex: "active",
        key: "active",
        align: "center",
        customRender(opt) {
          return h(Switch, {
            checked: opt.text,
            disabled: true,
          });
        },
      },
      {
        title: t("upload_limit"),
        dataIndex: "uploadLimit",
        key: "upload_limit",
        sorter: {
          multiple: 2,
        },
        customRender(opt) {
          return h(DSize, {
            value: opt.text,
          });
        },
      },
      {
        title: `${t("manage")} ${t("player")}`,
        align: "center",
        fixed: "right",
        key: "actions",
        customRender(opt) {
          return h(Space, [
            h(
              Tooltip,
              {
                title: t("edit"),
              },
              [
                h(
                  Button,
                  {
                    type: "primary",
                    onClick: () => alert("Under construction"),
                  },
                  {
                    icon: () => h(EditOutlined),
                  },
                ),
              ],
            ),
            h(
              Tooltip,
              {
                title: t("edit"),
              },
              [
                h(
                  Button,
                  {
                    onClick: () => alert("Under construction"),
                  },
                  {
                    icon: () => h(KeyOutlined),
                  },
                ),
              ],
            ),
            h(
              Popconfirm,
              {
                title: t("delete_player_confirm"),
                okText: t("yes"),
                cancelText: t("no"),
                onConfirm: () => alert("Under construction"),
              },
              h(
                Button,
                { danger: true },
                {
                  icon: () => h(DeleteOutlined),
                },
              ),
            ),
          ]);
        },
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
      result.value
        ? result.value.adminPlayers.edges.map((edge) => edge.node)
        : [],
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
              total: result.value ? result.value.adminPlayers.totalCount : 0,
            } as Pagination,
          }),
        ],
      );
  },
};
</script>
