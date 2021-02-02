<template>
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
</template>

<script>
import { useQuery } from "@vue/apollo-composable";
import gql from "graphql-tag";

export default {
  setup() {
    const { result, loading } = useQuery(gql`
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
    `);
    return { result, loading, json: JSON.stringify };
  },
};
</script>

<style>
</style>