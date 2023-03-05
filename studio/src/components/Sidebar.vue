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
  <a-layout-sider collapsed class="bg-transparent">
    <a-spin :spinning="loading">
      <a-menu
        v-model:selectedKeys="selectedKeys"
        mode="inline"
        class="upstage-menu"
      >
        <a-menu-item key="media">
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
        <a-menu-item
          key="admin"
          v-if="result?.whoami.roleName === 'Admin'"
          @click="iframeSrc = '/backstage/admin'"
        >
          <key-outlined />
          <span>Admin</span>
        </a-menu-item>
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

<style lang="less">
.upstage-menu {
  margin-top: 16px;
  margin-left: 16px;
  margin-right: 0;
  border-radius: 12px;

  .ant-menu-item {
    margin: 0;
    border-radius: 12px;

    &:active {
      background-color: transparent;
    }

    &.ant-menu-item-selected {
      background-color: #147d20;
      color: white;
    }
  }
}

.ant-tooltip-inner {
  [role="img"].anticon {
    margin-right: 8px;
  }
}
</style>
