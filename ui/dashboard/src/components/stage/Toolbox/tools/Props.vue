<template>
  <div class="columns" :style="'width: ' + props.length * 100 + 'px'">
    <div v-for="prop in props" :key="prop" class="column">
      <Skeleton :data="prop" />
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
    const props = store.state.stage.tools.props;
    console.log(props)
    return { props };
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