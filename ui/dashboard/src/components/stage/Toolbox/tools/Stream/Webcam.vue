<template>
  <Skeleton :data="object">
    <video @mousedown="capture" autoplay="true" ref="video"></video>
  </Skeleton>
</template>

<script>
import { ref } from "@vue/reactivity";
import Skeleton from "@/components/objects/Skeleton";
import { computed } from "@vue/runtime-core";
import { cropImageFromCanvas } from "@/utils/canvas";

export default {
  components: { Skeleton },
  setup: () => {
    const video = ref();
    if (navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices
        .getUserMedia({ video: true })
        .then(function (stream) {
          video.value.srcObject = stream;
        })
        .catch(function (error) {
          console.log("Something went wrong!", error);
        });
    }

    const image = ref();

    const capture = () => {
      const width = 100;
      const height = (width * video.value.videoHeight) / video.value.videoWidth;
      const canvas = document.createElement("canvas");
      canvas.width = width;
      canvas.height = height;
      canvas.getContext("2d").drawImage(video.value, 0, 0, width, height);
      image.value = cropImageFromCanvas(canvas).src;
    };

    const object = computed(() => ({
      src: image.value,
      type: "stream",
      isWebcam: true,
    }));

    return { video, object, capture };
  },
};
</script>

<style>
</style>