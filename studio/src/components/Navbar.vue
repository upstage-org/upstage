<script lang="ts" setup>
import Notifications from "components/Notifications.vue";
import LanguageSelector from "components/LanguageSelector.vue";
import configs from "config";
import logo from "assets/upstage.png";
import { inject } from "vue";
import type { ComputedRef } from "vue";
import type { User } from "models/studio";
import { WhoAmI } from "symbols";
import StudioVersion from "./StudioVersion.vue";

const to = (path: string) => `${configs.UPSTAGE_URL}/${path}`;
const whoami = inject<ComputedRef<User>>(WhoAmI);
</script>

<template>
  <a-space>
    <a
      :href="to('backstage/profile')"
      v-if="whoami"
      style="line-height: 0.8"
      class="text-right"
    >
      <span class="text-gray-500">{{ whoami.roleName }}</span>
      <a-typography-title :level="5" style="margin-bottom: 0">
        <span class="whitespace-nowrap">
          {{ whoami.displayName || whoami.username }}
        </span>
      </a-typography-title>
    </a>
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
          <a :href="to('backstage')">
            <a-menu-item>{{ $t("backstage") }}</a-menu-item>
          </a>
          <a :href="to('')">
            <a-menu-item>{{ $t("foyer") }}</a-menu-item>
          </a>
          <a-menu-item disabled> </a-menu-item>
        </a-menu>
      </template>
    </a-dropdown>
  </a-space>
</template>
