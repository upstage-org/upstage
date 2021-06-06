<template>
  <video v-if="playable" ref="video"></video>
  <img v-else src="@/assets/notfound.svg" />
</template>

<script>
import { computed, ref } from "@vue/runtime-core";
import { getSubsribeLink } from "@/utils/streaming";
import { useFlv } from "./objects/Streamer/composable";
export default {
  props: ["src"],
  setup: (props) => {
    const video = ref();
    const fullUrl = computed(() => getSubsribeLink(props.src));

    const { playable } = useFlv(video, fullUrl);
    return { video, playable };
  },
};
</script>

<style>
</style>