<script lang="ts" setup>
import { ref } from "vue";
import { useI18n } from "vue-i18n";
import { useRoute } from "vue-router";
import Entry from "./entry.vue";
import { h } from "vue";
import { useAsyncState } from "@vueuse/core";
import { configClient } from "services/graphql";
import { Skeleton } from "ant-design-vue";

const route = useRoute();
const activeKey = ref((route.params.section as string) || "foyer");
const { t } = useI18n();

const { state } = useAsyncState(
  configClient.query({
    foyer: {
      __scalar: true,
    },
    system: {
      enableDonate: true,
    },
  }),
  {
    foyer: null,
    system: null,
  }
);

const foyerConfigs = () =>
  state.value.foyer && state.value.system
    ? [
        h(Entry, {
          label: t("title"),
          name: "FOYER_TITLE",
          defaultValue: state.value.foyer?.title ?? "",
        }),
        h(Entry, {
          label: t("description"),
          multiline: true,
          name: "FOYER_DESCRIPTION",
          defaultValue: state.value.foyer?.description ?? "",
        }),
        h(Entry, {
          label: t("menu"),
          multiline: true,
          name: "FOYER_MENU",
          defaultValue: state.value.foyer?.menu ?? "",
          help: h("pre", { class: "text-sm" }, [
            `Syntax: "Title (URL)"
For example: Development (https://github.com/upstage-org/upstage/)
Put the navigation links line by line. Put > before the line to make it nested inside parent menu.
For example:
About
> FAQ (https://upstage.org.nz/?page_id=115)
> Contact (/contact)`,
          ]),
        }),
        h(Entry, {
          label: t("registration_button"),
          name: "SHOW_REGISTRATION",
          defaultValue: state.value.foyer?.showRegistration ?? false,
        }),
        h(Entry, {
          label: t("enable_upstage_donate"),
          name: "ENABLE_DONATE",
          defaultValue: state.value.system?.enableDonate ?? false,
        }),
      ]
    : [h(Skeleton)];
</script>

<template>
  <a-layout class="w-full shadow rounded-xl bg-white px-4 overflow-hidden">
    <a-tabs v-model:activeKey="activeKey">
      <a-tab-pane key="foyer" :tab="t('foyer_customisation')">
        <foyerConfigs />
      </a-tab-pane>
      <a-tab-pane key="system" :tab="t('system_configuration')"
        >Content of Tab Pane 2</a-tab-pane
      >
    </a-tabs>
  </a-layout>
</template>
