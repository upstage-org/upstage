<template>
  <div class="columns">
    <div
      v-for="background in backgrounds"
      :key="background"
      class="column"
      :class="{
        'has-background-primary': background.src === currentBackground,
      }"
    >
      <Image :src="background.src" @click="setBackground(background)" />
    </div>
  </div>
</template>

<script>
import Image from "@/components/Image";
import { useStore } from "vuex";
import { computed } from "vue";

export default {
  components: { Image },
  setup: () => {
    const store = useStore();

    const backgrounds = store.state.stage.tools.backdrops;

    const setBackground = (background) => {
      store.dispatch("stage/setBackground", background.src);
    };

    return {
      backgrounds,
      setBackground,
      currentBackground: computed(() => store.state.stage.background),
    };
  },
};
</script>

<style scoped>
.column {
  width: 160px;
  height: 90px;
  cursor: pointer;
}
</style>