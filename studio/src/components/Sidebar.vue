<script setup lang="ts">
import { computed, provide, ref } from "vue";
import { IsAdmin, WhoAmI } from "../symbols";
import { useQuery } from "@vue/apollo-composable";
import { StudioGraph } from "../models/studio";
import gql from "graphql-tag";
import configs from "../config";
import { useRouter } from "vue-router";
import { watch } from "vue";

const selectedMenu = ref(["stages"]);

const router = useRouter();

watch(selectedMenu, (value) => router.push(`/${value.join("/")}`));

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
    result.value?.whoami?.role ?? 0
  )
);

provide(
  WhoAmI,
  computed(() => result.value?.whoami)
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
        v-model:selectedKeys="selectedMenu"
        mode="inline"
        class="upstage-menu"
      >
        <a-menu-item key="media">
          <picture-outlined />&nbsp;
          <span>Media</span>
        </a-menu-item>
        <a-menu-item key="stages">
          <layout-outlined />
          <span>Stages</span>
        </a-menu-item>
        <a-menu-item key="legacy/backstage/profile/information">
          <user-outlined />
          <span>Profile</span>
        </a-menu-item>
        <a-sub-menu key="admin">
          <template #icon>
            <key-outlined />
          </template>
          <template #title>Admin</template>
          <a-menu-item key="admin/player">Player Management</a-menu-item>
          <a-menu-item key="legacy/backstage/admin/foyer-customisation"
            >Foyer Customisation</a-menu-item
          >
          <a-menu-item key="legacy/backstage/admin/email-notification"
            >Email Notification</a-menu-item
          >
          <a-menu-item key="legacy/backstage/admin/system-configuration"
            >System Configuration</a-menu-item
          >
        </a-sub-menu>
        <a-menu-item key="legacy/https://docs.upstage.live/">
          <book-outlined />
          <span>Manual</span>
        </a-menu-item>
      </a-menu>
    </a-spin>
  </a-layout-sider>
  <slot></slot>
</template>
