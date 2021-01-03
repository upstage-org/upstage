<template>
  <Image :src="data.src" @dragstart="dragstart" />
</template>

<script>
import { ref } from "vue";
import Image from "@/components/Image";
import dragghost from "@/assets/dragghost.png";

export default {
  props: ["data", "type"],
  components: { Image },
  setup: (props) => {
    const showCancelZone = ref(false);

    const dragstart = (e) => {
      showCancelZone.value = true;
      var img = new window.Image();
      img.src = dragghost;
      e.dataTransfer.setDragImage(img, 50, 50);
      e.dataTransfer.setData("avatar", JSON.stringify(props.data));
    };

    return { dragstart, showCancelZone };
  },
};
</script>

<style>
</style>