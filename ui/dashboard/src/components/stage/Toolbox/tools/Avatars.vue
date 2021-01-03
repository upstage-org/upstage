<template>
    <div v-for="avatar in avatars" :key="avatar">
      <Skeleton :data="avatar" />
    </div>
</template>

<script>
import Skeleton from "@/components/objects/Skeleton";
import { useStore } from "vuex";

export default {
  components: { Skeleton },
  setup: () => {
    const store = useStore();
    const avatars = store.state.stage.tools.avatars;
    return { avatars };
  },
};
</script>

<style scoped lang="scss">
</style>