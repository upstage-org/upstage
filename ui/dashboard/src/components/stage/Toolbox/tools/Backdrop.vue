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
    <div v-else>
      <div class="icon is-large"><Icon size="36" src="clear.svg" /></div>
      <span class="tag is-light is-block">Clear</span>
    </div>
  </div>
</template>

<script>
import { useStore } from "vuex";
import { computed } from "vue";
import Image from "@/components/Image";
import Icon from "@/components/Icon";

export default {
  components: { Image, Icon },
  setup: () => {
    const store = useStore();
    const currentBackground = computed(() => store.state.stage.background);

    const backgrounds = computed(() => {
      return [{ src: null }].concat(store.state.stage.tools.backdrops);
    });

    const setBackground = (background) => {
      store.dispatch("stage/setBackground", background.src);
    };

    return {
      backgrounds,
      setBackground,
      currentBackground,
    };
  },
};
</script>

<style scoped>
</style>