<script setup lang="ts">
import { apolloClient } from "apollo";
import { provide } from "@vue/runtime-core";
import Authorized from "components/Authorized.vue";
import Footer from "components/Footer.vue";
import Sidebar from "components/Sidebar.vue";
import { ref } from "vue";
import { SelectedMenu } from "symbols";
import Layout from "components/Layout.vue";
import { DefaultApolloClient } from "@vue/apollo-composable";

const selectedMenu = ref(["stage"]);

provide(DefaultApolloClient, apolloClient);
provide(SelectedMenu, selectedMenu);
</script>

<template>
  <Authorized>
    <a-layout>
      <Sidebar>
        <a-layout class="h-screen space-y-2 p-2">
          <Layout />
          <Footer />
        </a-layout>
      </Sidebar>
    </a-layout>
  </Authorized>
</template>
