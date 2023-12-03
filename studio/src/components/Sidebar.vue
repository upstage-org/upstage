<script setup lang="ts">
import { useRouter } from "vue-router";
import PlayerForm from "views/admin/player-management/PlayerForm.vue";
import { useUpdateProfile } from "hooks/auth";

const router = useRouter();

const { whoami, loading, save } = useUpdateProfile();
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
          :player="whoami"
          :onSave="save"
          :saving="loading"
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
