<script lang="ts">
import { useMutation, useQuery } from "@vue/apollo-composable";
import gql from "graphql-tag";
import { computed, reactive, watch, provide, ref, inject } from "vue";
import type { AdminPlayer, Media, Stage, StudioGraph } from "models/studio";
import { displayName, titleCase } from "utils/common";
import { ColumnType, TablePaginationConfig } from "ant-design-vue/lib/table";
import { SorterResult } from "ant-design-vue/lib/table/interface";
import { useI18n } from "vue-i18n";
import { Layout, Select, Space, Switch, Table, message } from "ant-design-vue";
import { FetchResult } from "@apollo/client/core";
import { h } from "vue";
import DDate from "components/display/DDate.vue";
import PlayerForm from "./PlayerForm.vue";
import ChangePassword from "./ChangePassword.vue";
import DeletePlayer from "./DeletePlayer.vue";
import type { DefaultOptionType } from "ant-design-vue/lib/select";
import Confirm from "components/Confirm.vue";
import { useUpdateUser } from "hooks/mutations";

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
    const enterStage = (stage: Stage) => {
      window.open(`/${stage.fileLocation}`, "_blank");
    };
    const tableParams = reactive({
      limit: 10,
      cursor: undefined,
      sort: ["CREATED_ON_ASC"],
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

    const { mutate, loading: saving } = useMutation<
      { authUser: { accessToken: string; refreshToken: string } },
      {}
    >(gql`
      mutation Login($username: String, $password: String) {
        authUser(username: $username, password: $password) {
          accessToken
          refreshToken
        }
      }
    `);

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
                lastLogin
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
      refresh();
    });

    const customLimit = ref("");

    const SWITCHABLE_ROLES = {
      GUEST: 4,
      PLAYER: 1,
      ADMIN: 8,
      SUPER_ADMIN: 32,
    };

    const columns: ColumnType<AdminPlayer>[] = [
      {
        title: t("role"),
        dataIndex: "role",
        key: "role",
        align: "center",
        sorter: {
          multiple: 1,
        },
        customRender(opt) {
          return h(
            Confirm,
            {
              title: `Are you sure you want to change ${displayName(
                opt.record,
              )}'s role?`,
              onConfirm: async ([value, selectedOption]: [
                number,
                DefaultOptionType,
              ]) => {
                await updateUser({
                  ...opt.record,
                  role: value,
                });
                message.success(
                  `Successfully switch ${displayName(opt.record)}'s role to ${
                    (selectedOption as DefaultOptionType).label
                  }!`,
                );
              },
            },
            {
              default: (slotProps: {
                confirm: (payload: [number, DefaultOptionType]) => void;
              }) =>
                h(Select, {
                  options: Object.entries(SWITCHABLE_ROLES).map(
                    ([key, id]) => ({
                      value: id,
                      label: titleCase(key),
                    }),
                  ),
                  value: opt.text,
                  onChange: (value, selectedOption) => {
                    slotProps.confirm([value as number, selectedOption]);
                  },
                }),
            },
          );
        },
      },
      {
        title: t("username"),
        key: "username",
        dataIndex: "username",
        sorter: {
          multiple: 2,
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
          multiple: 3,
        },
      },
      {
        title: t("last_login"),
        dataIndex: "lastLogin",
        key: "last_login",
        sorter: {
          multiple: 4,
        },
        customRender(opt) {
          return opt.text
            ? h(DDate, {
                value: opt.text,
              })
            : "";
        },
      },
      {
        title: t("date_registered"),
        dataIndex: "createdOn",
        key: "created_on",
        sorter: {
          multiple: 5,
        },
        customRender(opt) {
          return h(DDate, {
            value: opt.text,
          });
        },
        defaultSortOrder: "ascend",
      },
      {
        title: t("status"),
        dataIndex: "active",
        key: "active",
        align: "center",
        customRender(opt) {
          return h(Switch, {
            checked: opt.text,
            loading: savingUser.value,
            onChange: async (value) => {
              await updateUser({
                ...opt.record,
                active: !!value,
              });
              message.success(
                `Account ${displayName(opt.record)} ${
                  value ? "activated" : "deactivated"
                } successfully!`,
              );
            },
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
            h(PlayerForm, {
              player: opt.record,
              saving: savingUser.value,
              onSave: async (player: AdminPlayer) => {
                await updateUser({
                  ...player,
                });
                message.success(
                  `Successfully update ${displayName(player)}'s profile!`,
                );
              },
              disabledIntroduction: true,
            }),
            h(ChangePassword, {
              player: opt.record,
              saving: savingUser,
              onSave: async (player: AdminPlayer) => {
                await updateUser({
                  ...player,
                });
                message.success(
                  `Successfully reset ${displayName(player)}'s password!`,
                );
              },
            }),
            h(DeletePlayer, {
              player: opt.record,
              onDone: async (player: AdminPlayer) => {
                refresh();
                message.success(
                  `Successfully delete ${displayName(player)}'s account!`,
                );
              },
            }),
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

    const refresh = () => {
      fetchMore({
        variables: params.value,
        updateQuery,
      });
    };
    provide("refresh", refresh);

    const {
      mutate: updateUser,
      loading: savingUser,
      onDone: onUserUpdated,
      onError: onUserUpdateError,
    } = useUpdateUser();

    const handleUpdate = (result: FetchResult) => {
      if (result.errors) {
        message.error("You don't have permission to perform this action!");
      } else {
        refresh();
      }
    };

    onUserUpdated(handleUpdate);

    return () =>
      h(
        Layout,
        {
          class: "w-full shadow rounded-xl bg-white overflow-hidden",
        },
        [
          h(Table, {
            class: "w-full overflow-auto",
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
