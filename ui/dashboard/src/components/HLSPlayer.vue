<template>
  <video v-bind="$attrs" v-if="isSupported" ref="video"></video>
  <img v-else src="@/assets/notfound.svg" />
</template>

<script>
import { ref } from "@vue/reactivity";
import { computed, onMounted, watch } from "@vue/runtime-core";
import Hls from "hls.js";
export default {
  props: {
    src: String,
  },
  setup(props) {
    const video = ref();
    const isSupported = computed(() => Hls.isSupported());

    const initPlayer = () => {
      if (isSupported.value) {
        const hls = new Hls();
        hls.loadSource(props.src);
        hls.attachMedia(video.value);
      }
    };

    onMounted(initPlayer);
    watch(() => props.src, initPlayer);

    return { video, isSupported };
  },
};
</script>

<style>
</style>