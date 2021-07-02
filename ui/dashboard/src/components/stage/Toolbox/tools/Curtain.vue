<template>
  <div @click="toggleCurtain(null)">
    <div class="icon is-large"><Icon size="36" src="clear.svg" /></div>
    <span class="tag is-light is-block">No curtain</span>
  </div>
  <div
    v-for="curtain in curtains"
    :key="curtain"
    :class="{
      active: curtain.src === currentCurtain,
    }"
  >
    <Image
      :src="curtain.src"
      :title="curtain.name"
      @click="toggleCurtain(curtain.src)"
    />
  </div>
</template>

<script>
import { useStore } from "vuex";
import Image from "@/components/Image";
import Icon from "@/components/Icon";
import { computed } from "@vue/runtime-core";

export default {
  components: { Image, Icon },
  setup: () => {
    const store = useStore();
    const curtains = store.state.stage.tools.curtains;

    const currentCurtain = computed(() => store.state.stage.curtain);
    const toggleCurtain = (curtain) => {
      if (currentCurtain.value === curtain) {
        store.dispatch("stage/drawCurtain", null);
      } else {
        store.dispatch("stage/drawCurtain", curtain);
      }
    };

    return { curtains, toggleCurtain, currentCurtain };
  },
};
</script>

<style scoped lang="scss">
</style>