<script setup lang="ts">
import { computed, provide } from "vue";
import { IsAdmin, WhoAmI } from "../symbols";
import { useQuery } from "@vue/apollo-composable";
import { AdminPlayer, StudioGraph } from "../models/studio";
import gql from "graphql-tag";
import configs from "../config";
import { useRouter } from "vue-router";
import PlayerForm from "views/admin/player-management/PlayerForm.vue";
import { useUpdateUser } from "hooks/mutations";
import { message } from "ant-design-vue";

const router = useRouter();

const { result, loading } = useQuery<StudioGraph>(gql`
  query WhoAmI {
    whoami {
      id
      username
      firstName
      lastName
      displayName
      email
      role
      roleName
      uploadLimit
      active
      intro
    }
  }
`);

const isAdmin = computed(() =>
  [configs.ROLES.ADMIN, configs.ROLES.SUPER_ADMIN].includes(
    result.value?.whoami?.role ?? 0,
  ),
);

const whoami = computed(() => result.value?.whoami);

provide(WhoAmI, whoami);
provide(IsAdmin, isAdmin);

const {
  mutate: updateUser,
  loading: savingUser,
  onDone: onUserUpdated,
  onError: onUserUpdateError,
} = useUpdateUser();

const handleSaveProfile = async (player: AdminPlayer) => {
  await updateUser({
    ...player,
  });
  message.success(`Successfully update your profile!`);
};
</script>

<template>
  <a-layout-sider
    theme="light"
    collapsible
    collapsed
    class="select-none"
    width="240"
  >
    <a-spin :spinning="loading">
      <a-menu
        :selected-keys="[router.currentRoute.value.path]"
        @select="router.push($event.key.toString())"
        mode="inline"
        class="upstage-menu"
      >
        <a-menu-item key="/media">
          <picture-outlined />&nbsp;
          <span>Media</span>
        </a-menu-item>
        <a-menu-item key="/stages">
          <layout-outlined />
          <span>Stages</span>
        </a-menu-item>
        <PlayerForm
          v-if="whoami"
          :player="whoami as AdminPlayer"
          :onSave="handleSaveProfile"
          :saving="savingUser"
          noUploadLimit
          noStatusToggle
          v-slot="{ onClick }"
        >
          <a-menu-item :onClick="onClick">
            <user-outlined />
            <span>Profile</span>
          </a-menu-item>
        </PlayerForm>
        <a-sub-menu key="admin">
          <template #icon>
            <key-outlined />
          </template>
          <template #title>Admin</template>
          <a-menu-item key="/admin/player">Player Management</a-menu-item>
          <a-menu-item key="/legacy/backstage/admin/foyer-customisation"
            >Foyer Customisation</a-menu-item
          >
          <a-menu-item key="/legacy/backstage/admin/email-notification"
            >Email Notification</a-menu-item
          >
          <a-menu-item key="/legacy/backstage/admin/system-configuration"
            >System Configuration</a-menu-item
          >
        </a-sub-menu>
        <a-menu-item key="/legacy/https://docs.upstage.live/">
          <book-outlined />
          <span>Manual</span>
        </a-menu-item>
      </a-menu>
    </a-spin>
  </a-layout-sider>
  <slot></slot>
</template>
