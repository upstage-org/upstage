<script lang="ts" setup>
import Notifications from "components/Notifications.vue";
import LanguageSelector from "components/LanguageSelector.vue";
import configs from "config";
import logo from "assets/upstage.png";
import StudioVersion from "./StudioVersion.vue";
import { useUpdateProfile, useLogout } from "hooks/auth";
import PlayerForm from "views/admin/player-management/PlayerForm.vue";

const to = (path: string) => `${configs.UPSTAGE_URL}/${path}`;

const { whoami, save } = await useUpdateProfile();

const logout = useLogout();
</script>

<template>
  <a-space>
    <PlayerForm
      v-if="whoami"
      :player="whoami"
      :onSave="save"
      :saving="true"
      noUploadLimit
      noStatusToggle
      v-slot="{ onClick }"
    >
      <div :onClick="onClick" class="cursor-pointer">
        <span class="text-gray-500 cursor-pointer">{{ whoami.roleName }}</span>
        <a-typography-title :level="5" style="margin-bottom: 0">
          <span class="whitespace-nowrap">
            {{ whoami.displayName || whoami.username }}
          </span>
        </a-typography-title>
      </div>
    </PlayerForm>
    <Notifications />
    <a-space direction="vertical">
      <LanguageSelector />
      <StudioVersion />
    </a-space>
    <a-dropdown class="ml-4">
      <a class="ant-dropdown-link flex-nowrap block w-24" @click.prevent>
        <img :src="logo" class="h-6" />
        <down-outlined />
      </a>
      <template #overlay>
        <a-menu>
          <a :href="to('')">
            <a-menu-item>{{ $t("foyer") }}</a-menu-item>
          </a>
          <a-menu-item @click="logout">{{ $t("logout") }}</a-menu-item>
        </a-menu>
      </template>
    </a-dropdown>
  </a-space>
</template>
