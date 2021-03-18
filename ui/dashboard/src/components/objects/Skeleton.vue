<template>
  <div
    class="is-flex is-align-items-center"
    draggable="true"
    @dragstart="dragstart"
    @touchmove="touchmove"
    @touchend="touchend"
    :style="{
      position: position.isDragging ? 'fixed' : 'static',
      width: position.isDragging ? '100px' : '100%',
      height: position.isDragging ? '100px' : '100%',
      top: position.y - topbarPosition.top + 'px',
      left: position.x - topbarPosition.left + 'px',
    }"
    :title="data.name"
  >
    <slot v-if="$slots.default" />
    <Image v-else :src="data.src" />
    <Icon
      v-if="data.multi"
      class="is-multi"
      title="This is a multiframe avatar"
      src="multi-frame.svg"
    />
  </div>
</template>

<script>
import { reactive, ref } from "vue";
import Image from "@/components/Image";
import Icon from "@/components/Icon";
import { useStore } from "vuex";

export default {
  props: ["data", "type"],
  components: { Image, Icon },
  setup: (props) => {
    const store = useStore();
    const position = reactive({
      isDragging: false,
    });
    const topbarPosition = ref({});

    const dragstart = (e) => {
      e.dataTransfer.setData("object", JSON.stringify(props.data));
    };

    const touchmove = (e) => {
      position.isDragging = true;
      position.x = e.changedTouches[0]?.clientX - 50;
      position.y = e.changedTouches[0]?.clientY - 50;
      const topbar = document.getElementById("topbar");
      if (topbar) {
        topbarPosition.value = topbar.getBoundingClientRect();
      }
    };

    const touchend = () => {
      position.isDragging = false;
      store.dispatch("stage/placeObjectOnStage", {
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
.is-multi {
  position: relative;
  left: -20px;
  top: 30px;
}
</style>