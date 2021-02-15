<template>
  <div>
    View Scenes wireframes
    <a
      href="https://github.com/upstage-org/mobilise/issues/64#issuecomment-740554084"
      target="_blank"
      >here</a
    >
    <div v-if="loading">Loading...</div>
    <div v-else>
      {{ json(result) }}
    </div>
  </div>
</template>

<script>
import { onMounted, ref } from "vue";
import { client } from "@/services/graphql";
import { gql } from "graphql-request";
export default {
  setup() {
    const loading = ref(true);
    const result = ref();

    onMounted(async () => {
      result.value = await client.request(
        gql`
          query Posts {
            posts {
              data {
                id
                title
              }
              meta {
                totalCount
              }
            }
          }
        `
      );
      loading.value = false;
    });

    return { result, loading, json: JSON.stringify };
  },
};
</script>

<style>
</style>