<template>
  <video v-if="playable" ref="video"></video>
  <img v-else src="@/assets/notfound.svg" />
</template>

<script>
import { computed, ref, onMounted } from "vue";
import { getSubsribeLink } from "@/utils/streaming";
import { useFlv } from "./objects/Streamer/composable";
export default {
  props: ["src"],
  emits: ["scan"],
  setup: (props, { emit }) => {
    const video = ref();
    const fullUrl = computed(() => getSubsribeLink(props.src));

    const { playable } = useFlv(video, fullUrl);
    onMounted(() => {
      video.value.addEventListener("loadedmetadata", () => {
        emit("scan", {
          width: video.value.videoWidth,
          height: video.value.videoHeight,
          duration: video.value.duration,
          video: video.value,
        });
      });
    });
    return { video, playable };
  },
};
</script>

<style></style>
