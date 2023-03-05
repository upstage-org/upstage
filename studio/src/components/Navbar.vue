<script lang="ts" setup>
import Notifications from "components/Notifications.vue";
import LanguageSelector from "components/LanguageSelector.vue";
import configs from "config";
import logo from "assets/upstage.png";

const to = (path: string) => `${configs.UPSTAGE_URL}/${path}`;
</script>

<template>
  <a-space>
    <Notifications />
    <LanguageSelector />
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
        </a-menu>
      </template>
    </a-dropdown>
  </a-space>
</template>
