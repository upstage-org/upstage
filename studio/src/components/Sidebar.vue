<script setup lang="ts">
import { computed, inject, provide, ref } from "vue";
import { IframeSrc, IsAdmin, SelectedMenu, WhoAmI } from "../symbols";
import { useQuery } from "@vue/apollo-composable";
import { StudioGraph } from "../models/studio";
import gql from "graphql-tag";
import configs from "../config";

const selectedKeys = inject<string[]>(SelectedMenu);
const iframeSrc = ref("");
provide(IframeSrc, iframeSrc);

const { result, loading } = useQuery<StudioGraph>(gql`
  query WhoAmI {
    whoami {
      username
      displayName
      role
      roleName
      uploadLimit
    }
  }
`);

const isAdmin = computed(() =>
  [configs.ROLES.ADMIN, configs.ROLES.SUPER_ADMIN].includes(
    result.value?.whoami?.role ?? 0,
  ),
);

provide(
  WhoAmI,
  computed(() => result.value?.whoami),
);
provide(IsAdmin, isAdmin);
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
        v-model:selectedKeys="selectedKeys"
        mode="inline"
        class="upstage-menu"
      >
        <a-menu-item key="media" @click="iframeSrc = ''">
          <picture-outlined />&nbsp;
          <span>Media</span>
        </a-menu-item>
        <a-menu-item key="stage" @click="iframeSrc = ''">
          <layout-outlined />
          <span>Stages</span>
        </a-menu-item>
        <a-menu-item
          key="profile"
          @click="iframeSrc = '/backstage/profile/information'"
        >
          <user-outlined />
          <span>Profile</span>
        </a-menu-item>
        <a-sub-menu key="admin">
          <template #icon>
            <key-outlined />
          </template>
          <template #title>Admin</template>
          <a-menu-item key="admin/player" @click="iframeSrc = ''"
            >Player Management</a-menu-item
          >
          <a-menu-item
            key="admin/batch"
            @click="iframeSrc = '/backstage/admin/batch-user-creation'"
            >Batch User Creation</a-menu-item
          >
          <a-menu-item
            key="admin/foyer"
            @click="iframeSrc = '/backstage/admin/foyer-customisation'"
            >Foyer Customisation</a-menu-item
          >
          <a-menu-item
            key="admin/email"
            @click="iframeSrc = '/backstage/admin/email-notification'"
            >Email Notification</a-menu-item
          >
          <a-menu-item
            key="admin/system"
            @click="iframeSrc = '/backstage/admin/system-configuration'"
            >System Configuration</a-menu-item
          >
        </a-sub-menu>
        <a-menu-item
          key="manual"
          href="https://docs.upstage.live/"
          @click="iframeSrc = 'https://docs.upstage.live/'"
        >
          <book-outlined />
          <span>Manual</span>
        </a-menu-item>
      </a-menu>
    </a-spin>
  </a-layout-sider>
  <slot></slot>
</template>
