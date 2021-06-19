<template>
  <div
    class="is-flex is-align-items-center"
    draggable="true"
    @dragstart="dragstart"
    @dragend="dragend"
    @dragenter.prevent
    @dragover.prevent
    @drop.prevent="drop"
    @touchmove="touchmove"
    @touchend="touchend"
    @dblclick="hold"
    @mouseenter="showMovable"
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
    <SavedDrawing v-else-if="data.type === 'drawing'" :drawing="data" />
    <p
      v-else-if="data.type === 'text'"
      :style="{
        ...data,
        transform: `scale(${76 / data.w})`,
        'transform-origin': 0,
      }"
      v-html="data.content"
    ></p>
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
import { useStore } from "vuex";
import { computed, reactive, ref } from "vue";
import Image from "@/components/Image";
import Icon from "@/components/Icon";
import SavedDrawing from "./tools/Draw/SavedDrawing";

export default {
  props: ["data", "real", "ghost"],
  components: { Image, Icon, SavedDrawing },
  setup: (props) => {
    const store = useStore();
    const position = reactive({
      isDragging: false,
    });
    const topbarPosition = ref({});

    const dragstart = (e) => {
      e.dataTransfer.setData(
        "text",
        JSON.stringify({ object: props.data, isReal: props.real })
      );
    };

    const dragend = () => {
      if (props.real) {
        store.commit("stage/SET_ACTIVE_MOVABLE", null);
      }
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
      store.dispatch(
        props.real ? "stage/shapeObject" : "stage/placeObjectOnStage",
        {
          ...props.data,
          x: position.x,
          y: position.y,
        }
      );
    };

    const holdable = computed(() =>
      ["avatar", "drawing"].includes(props.data.type)
    );
    const hold = () => {
      if (props.real && holdable.value && !props.data.holder) {
        store.dispatch("user/setAvatarId", props.data.id);
      }
    };
    const showMovable = () => {
      if (
        props.real &&
        (!props.data.holder ||
          !holdable.value ||
          props.data.holder.id === store.state.stage.session)
      ) {
        store.commit("stage/SET_ACTIVE_MOVABLE", props.data.id);
      }
    };

    const drop = (e) => {
      if (props.real) {
        const { object } = JSON.parse(e.dataTransfer.getData("text"));
        store.dispatch("stage/bringToFrontOf", {
          front: object.id,
          back: props.data.id,
        });
      }
    };

    return {
      dragstart,
      dragend,
      touchmove,
      touchend,
      position,
      topbarPosition,
      hold,
      showMovable,
      drop,
    };
  },
};
</script>

<style>
</style>