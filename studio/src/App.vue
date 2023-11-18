<script setup lang="ts">
import { apolloClient } from "apollo";
import { provide } from "@vue/runtime-core";
import Authorized from "components/Authorized.vue";
import Sidebar from "components/Sidebar.vue";
import { DefaultApolloClient } from "@vue/apollo-composable";

provide(DefaultApolloClient, apolloClient);
</script>

<template>
  <a-config-provider
    :theme="{
      token: {
        colorPrimary: '#007011',
        borderRadius: 4,
        fontSize: 16,
        fontFamily: 'Josefin Sans, sans-serif',
        colorPrimaryBg: '#ffffff',
      },
      components: {},
    }"
  >
    <Authorized>
      <a-layout>
        <Sidebar>
          <a-layout class="h-screen space-y-2 p-2">
            <router-view />
          </a-layout>
        </Sidebar>
      </a-layout>
    </Authorized>
  </a-config-provider>
</template>
