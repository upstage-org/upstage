<template>
  <Skeleton v-if="loading" height="24px" />
  <span v-else class="tag is-dark is-small">
    <span class="icon">
      <i class="fas fa-user"></i>
    </span>
    <span>{{ players }}</span>
    <span class="icon">
      <i class="fas fa-desktop"></i>
    </span>
    <span>{{ audiences }}</span>
  </span>
</template>

<script>
import Skeleton from "@/components/Skeleton";
import { useCounter } from "./composable";
export default {
  props: ["stageUrl"],
  components: { Skeleton },
  setup(props) {
    const [players, audiences, loading] = useCounter(props.stageUrl);
    return { players, audiences, loading };
  },
};
</script>

<style>
</style>