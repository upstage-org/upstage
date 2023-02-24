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
  <MediaTable v-if="result.selectedMenu === 'media'">
    <MediaUpload />
  </MediaTable>
  <StageTable v-if="result.selectedMenu === 'stage'" />
  <div class="tobe-integrating" v-if="result.selectedMenu === 'profile'">
    <iframe class="bg-gray-200" src="/backstage/profile/information" />
  </div>
  <div class="tobe-integrating" v-if="result.selectedMenu === 'admin'">
    <iframe class="bg-gray-200" src="/backstage/admin" />
  </div>
  <div class="tobe-integrating" v-if="result.selectedMenu === 'manual'">
    <iframe class="bg-gray-200" src="https://docs.upstage.live/" />
  </div>
</template>

<style lang="less" scoped>
.tobe-integrating {
  padding: 16px;
  padding-bottom: 0;
  height: 100%;

  iframe {
    width: 100%;
    height: 100%;
    border-radius: 12px;
    border: none;
  }
}
</style>
