<template>
  <div class="columns">
    <div v-for="background in backgrounds" :key="background" class="column">
      <Image :src="background.src" />
    </div>
  </div>
</template>

<script>
import config from "@/../vue.config";
import Image from "@/components/Image";

export default {
  components: { Image },
  setup: () => {
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

    return { backgrounds };
  },
};
</script>

<style scoped>
.column {
  width: 160px;
  height: 90px;
}
</style>