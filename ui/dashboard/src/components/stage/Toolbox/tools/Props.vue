<template>
  <div v-for="prop in props" :key="prop">
    <Skeleton :data="prop" />
  </div>
</template>

<script>
import Skeleton from "@/components/objects/Skeleton";
import { useStore } from "vuex";

export default {
  components: { Skeleton },
  setup: () => {
    const store = useStore();
    const props = store.state.stage.tools.props;
    return { props };
  },
};
</script>

<style scoped lang="scss">
</style>