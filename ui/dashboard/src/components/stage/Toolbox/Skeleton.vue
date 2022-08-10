<template>
  <div class="is-flex is-align-items-center is-justify-content-center skeleton" :class="{ dropzone }" draggable="true" @dragstart="dragstart"
    @dragend="dragend" @dragenter.prevent @dragover.prevent="dropzone = true" @dragleave.prevent="dropzone = false"
    @drop.prevent="drop" @touchmove="touchmove" @touchend="touchend" @dblclick="hold" @mouseenter="showMovable" :style="{
      position: position.isDragging ? 'fixed' : 'static',
      width: position.isDragging ? '100px' : '100%',
      height: position.isDragging ? '100px' : '100%',
      top: position.y - topbarPosition.top + 'px',
      left: position.x - topbarPosition.left + 'px',
    }" :title="data.name">
    <slot v-if="$slots.default" />
    <SavedDrawing v-else-if="data.drawingId" :drawing="data" />
    <p v-else-if="data.type === 'text'" :style="{
      ...data,
      transform: `scale(${76 / data.w})`,
      'transform-origin': 0,
    }" v-html="data.content"></p>
    <div :title="`Stream key: ${data.name}`" class="is-fullwidth" v-else-if="data.type === 'stream'">
      <Icon src="stream.svg" size="36" />
      <span class="tag is-light is-block stream-key">{{ data.name }}</span>
    </div>
    <div v-else-if="data.type === 'meeting'" class="is-flex-grow-1 pt-2">
      <Icon src="meeting.svg" size="48" />
      <span class="tag is-light is-block stream-key">{{ data.name }}</span>
    </div>
    <Image v-else :src="data.src" />
    <Icon v-if="data.multi" class="is-multi" title="This is a multiframe avatar" src="multi-frame.svg" />
  </div>
</template>

<script>
import { useStore } from "vuex";
import { computed, reactive, ref } from "vue";
import Image from "@/components/Image";
import Icon from "@/components/Icon";
import SavedDrawing from "./tools/Draw/SavedDrawing";

export default {
  props: {
    data: {
      type: Object,
      required: true,
    },
    real: {
      type: Boolean,
      default: false,
    },
    ghost: {
      type: Boolean,
      default: false,
    },
    nodrop: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["dragstart"],
  components: { Image, Icon, SavedDrawing },
  setup: (props, { emit }) => {
    const store = useStore();
    const position = reactive({
      isDragging: false,
    });
    const topbarPosition = ref({});

    const dragstart = (e) => {
      e.dataTransfer.setData(
        "text",
        JSON.stringify({ object: props.data, isReal: props.real, nodrop: props.nodrop })
      );
      document.getElementById('meeting-room')?.classList.add('disable-pointer')
      emit("dragstart", e);
    };

    const dragend = () => {
      document.getElementById('meeting-room')?.classList.remove('disable-pointer')
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
      ["avatar"].includes(props.data.type)
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
      dropzone.value = false;
      const { object } = JSON.parse(e.dataTransfer.getData("text"));
      if (props.real) {
        store.dispatch("stage/bringToFrontOf", {
          front: object.id,
          back: props.data.id,
        });
      } else {
        // Re-order toolbox
        store.commit("stage/REORDER_TOOLBOX", {
          from: object,
          to: props.data,
        });
      }
    };

    const dropzone = ref(false);

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
      dropzone
    };
  },
};
</script>

<style scoped lang="scss">
.stream-key {
  width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
}

.skeleton {
  >* {
    transition-duration: 0.25s;
  }
}

.dropzone {
  background: repeating-radial-gradient(circle,
      green,
      green 10px,
      #007011 10px,
      #007011 20px);

  >* {
    transform: translateX(50%) !important;
  }
}
</style>
