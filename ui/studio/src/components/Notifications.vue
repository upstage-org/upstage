<script lang="ts" setup>
import { useQuery } from "@vue/apollo-composable";
import gql from "graphql-tag";
import { computed } from "vue";
import { permissionFragment } from "models/fragment";
import { StudioGraph } from "models/studio";
import { absolutePath } from "utils/common";
import { useConfirmPermission } from "./table/media/MediaForm/composable";

const { result, loading, refetch } = useQuery<StudioGraph>(gql`
  {
    notifications {
      type
      mediaUsage {
        ...permissionFragment
        asset {
          name
          src
        }
      }
    }
  }
  ${permissionFragment}
`);

const notifications = computed(() => result.value?.notifications || []);
const { mutate: confirmPermission } = useConfirmPermission();
const refresh = () => refetch();
</script>

<template>
  <a-popover title="Notifications" trigger="click">
    <template #content>
      <a-list class="w-96 overflow-auto" style="max-height: 75vh">
        <a-list-item
          v-for="(notification, i) in notifications"
          :key="i"
          class="px-4"
        >
          <template v-if="notification.type === 'MEDIA_USAGE'">
            <a-list-item-meta>
              <template #avatar>
                <a-avatar
                  class="my-2"
                  :src="absolutePath(notification.mediaUsage.asset.src)"
                />
              </template>
              <template #title>
                <div class="text-sm whitespace-pre-wrap mb-2">
                  <b>
                    <DName :user="notification.mediaUsage.user" />
                  </b>
                  is requesting access to your media
                  <b>{{ notification.mediaUsage.asset.name }}</b>
                  :
                  <em>&quot;{{ notification.mediaUsage.note }}&quot;</em>
                  <br />
                </div>
                <a-space>
                  <smart-button
                    type="primary"
                    :action="
                      () =>
                        confirmPermission({
                          approved: true,
                          id: notification.mediaUsage.id,
                        }).then(refresh)
                    "
                    >{{ $t("approve") }}</smart-button
                  >
                  <smart-button
                    type="danger"
                    :action="
                      () =>
                        confirmPermission({
                          approved: false,
                          id: notification.mediaUsage.id,
                        }).then(refresh)
                    "
                    >{{ $t("reject") }}</smart-button
                  >
                </a-space>
              </template>
              <template #description>
                <d-date :value="notification.mediaUsage.createdOn" />
              </template>
            </a-list-item-meta>
          </template>
        </a-list-item>
      </a-list>
    </template>
    <a-badge :count="notifications.length" class="relative top-1">
      <a-button type="text">
        <a-spin v-if="loading" />
        <NotificationFilled v-else />
      </a-button>
    </a-badge>
  </a-popover>
</template>
