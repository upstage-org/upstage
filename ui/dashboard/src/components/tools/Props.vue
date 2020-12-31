<template>
  <div class="columns">
    <div v-for="prop in props" :key="prop" class="column">
      <Image :src="prop.src" fit="contain" />
    </div>
  </div>
</template>

<script>
import Image from "@/components/Image";
import config from "@/../vue.config";

export default {
  components: { Image },
  setup: () => {
    const files = ["facemask_filter.png", "quarantini_clearcut.png"];
    const props = files.map((file) => ({
      name: file,
      src: `${config.publicPath}demo/props/${file}`,
    }));
    return { props };
  },
};
</script>

<style scoped>
.column {
  width: 160px;
  height: 90px;
}
</style>