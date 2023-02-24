<script setup lang="ts">
import { apolloClient } from "apollo";
import { provide } from "@vue/runtime-core";
import { DefaultApolloClient } from "@vue/apollo-composable";
import Authorized from "components/Authorized.vue";
import Dropzone from "components/Dropzone.vue";
import Footer from "components/Footer.vue";
import Sidebar from "components/Sidebar.vue";
import EntryTable from "components/table/EntryTable.vue";
import EntryFilter from "components/filter/EntryFilter.vue";

provide(DefaultApolloClient, apolloClient);
</script>

<template>
  <Authorized>
    <a-layout>
      <Sidebar />
      <a-layout class="h-screen">
        <Dropzone>
          <EntryFilter />
          <EntryTable />
        </Dropzone>
        <Footer />
      </a-layout>
    </a-layout>
  </Authorized>
</template>
