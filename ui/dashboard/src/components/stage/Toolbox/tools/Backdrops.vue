<template>
  <div
    v-for="background in backgrounds"
    :key="background"
    :class="{
      active: background.src === currentBackground,
    }"
    @click="setBackground(background)"
  >
    <Image v-if="background.src" :src="background.src" />
    <Image v-else :src="dragghost" />
  </div>
</template>

<script>
import Image from "@/components/Image";
import { useStore } from "vuex";
import { computed } from "vue";
import dragghost from "@/assets/dragghost.png";

export default {
  components: { Image },
  setup: () => {
    const store = useStore();
    const currentBackground = computed(() => store.state.stage.background);

    const backgrounds = computed(() => {
      return [{ src: null }].concat(store.state.stage.tools.backdrops);
    });

    const setBackground = (background) => {
      store.dispatch("stage/setBackground", background.src);
    };

    console.log(currentBackground.value);

    return {
      backgrounds,
      setBackground,
      currentBackground,
      dragghost,
    };
  },
};
</script>

<style scoped>
</style>