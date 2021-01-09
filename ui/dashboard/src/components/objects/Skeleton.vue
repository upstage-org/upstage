<template>
  <Image
    :src="data.src"
    @dragstart="dragstart"
    @drag="drag"
    @touchmove="touchmove"
    @touchend="touchend"
    :style="{
      position: position.isDragging ? 'fixed' : 'static',
      top: position.y - topbarPosition.top + 'px',
      left: position.x - topbarPosition.left + 'px',
      width: '100px',
    }"
  />
</template>

<script>
import { reactive, ref } from "vue";
import Image from "@/components/Image";
import dragghost from "@/assets/dragghost.png";
import { useStore } from "vuex";

export default {
  props: ["data", "type"],
  components: { Image },
  setup: (props) => {
    const store = useStore();
    const position = reactive({
      isDragging: false,
    });
    const topbarPosition = ref({});

    const dragstart = (e) => {
      var img = new window.Image();
      img.src = dragghost;
      e.dataTransfer.setDragImage(img, 50, 50);
      e.dataTransfer.setData("avatar", JSON.stringify(props.data));
    };

    const touchmove = (e) => {
      position.isDragging = true;
      position.x = e.changedTouches[0]?.clientX - 50;
      position.y = e.changedTouches[0]?.clientY - 50;
      topbarPosition.value = document
        .getElementById("topbar")
        .getBoundingClientRect();
    };

    const touchend = () => {
      position.isDragging = false;
      store.dispatch("stage/summonAvatar", {
        ...props.data,
        x: position.x,
        y: position.y,
      });
    };

    return { dragstart, touchmove, touchend, position, topbarPosition };
  },
};
</script>

<style>
</style>