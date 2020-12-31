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
      <Image
        :src="background.src"
        @click="setBackground(background)"
        fit="contain"
      />
    </div>
  </div>
</template>

<script>
import config from "@/../vue.config";
import Image from "@/components/Image";
import { useStore } from "vuex";
import { computed } from "vue";

export default {
  components: { Image },
  setup: () => {
    const store = useStore();
    const backgrounds = [
      {
        name: "1",
        src: config.publicPath + "demo/backdrops/1.jpg",
      },
      {
        name: "2",
        src: config.publicPath + "demo/backdrops/2.jpg",
      },
      {
        name: "3",
        src: config.publicPath + "demo/backdrops/3.jpg",
      },
      {
        name: "4",
        src: config.publicPath + "demo/backdrops/4.jpg",
      },
    ];

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