<script lang="ts" setup>
import { useQuery } from "@vue/apollo-composable";
import gql from "graphql-tag";

const { result } = useQuery(
  gql`
    {
      selectedMenu @client
    }
  `
);
</script>

<template>
  <MediaFilter v-if="result.selectedMenu === 'media'" />
  <MediaFilter v-if="result.selectedMenu === 'stage'" />
</template>
