<template>
  <div class="columns" :style="'width: ' + avatars.length * 100 + 'px'">
    <div v-for="avatar in avatars" :key="avatar" class="column">
      <Skeleton :data="avatar" />
    </div>
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
.column {
  width: 160px;
  height: 90px;

  &:hover {
    background-color: hsl(0, 0%, 71%);
    cursor: pointer;
    border-radius: 5px;
  }
}
</style>