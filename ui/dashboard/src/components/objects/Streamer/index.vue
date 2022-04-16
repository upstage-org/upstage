<template>
  <div>
    <Object :object="stream">
      <template #menu="slotProps">
        <MenuContent :object="object" :stream="stream" v-bind="slotProps" v-model:active="active" />
      </template>

      <template #render>
        <Loading v-if="loading" height="100%" />
        <video v-bind:id="'video' + stream.id" v-show="!loading" ref="video" :src="object.url" :muted="localMuted"
          preload="auto" disablepictureinpicture @loadeddata="loadeddata" @ended="stream.isPlaying = false" :style="{
            'border-radius': stream.shape === 'circle' ? '100%' : 0,
          }"></video>
        <button v-if="isPlayer" class="button is-small mute-icon clickable" @mousedown="toggleMuted">
          <i v-if="localMuted" class="fas fa-volume-mute has-text-danger"></i>
          <i v-else class="fas fa-volume-up has-text-primary"></i>
        </button>
      </template>
    </Object>
  </div>
</template>

<script>
import { computed, reactive, ref, watch } from "vue";
import Object from "../Object.vue";
import { useStore } from "vuex";
import { useFlv, useCatchup } from "./composable";
import { getSubsribeLink } from "@/utils/streaming";
import Loading from "@/components/Loading.vue";
import MenuContent from '../Avatar/ContextMenu'

export default {
  components: { Object, Loading, MenuContent },
  emits: ["update:active", "hold"],
  props: ["object", "setSliderMode",],
  setup: (props) => {
    const store = useStore();
    const shapes = computed(() => store.state.stage.tools.shapes);

    const stream = reactive({ ...props.object, isPlaying: true, src: loading });
    const video = ref();
    const isPlayer = computed(() => store.getters["stage/canPlay"]);

    const synchronize = () => {
      if (stream.isPlaying && video.value) {
        video.value.play();
      } else {
        video.value.pause();
      }
    };

    watch(
      () => props.object,
      () => {
        window.Object.assign(stream, props.object);
        synchronize();
      }
    );
    const loading = ref(true);
    const loadeddata = () => {
      loading.value = false;
      synchronize();
    };

    if (props.object.isRTMP) {
      const fullUrl = computed(() => getSubsribeLink(props.object.url));
      useCatchup(video);
      const { playable } = useFlv(video, fullUrl);

      watch(playable, value => {
        console.log("playable", value);
        if (!value) {
          store.dispatch("stage/deleteObject", props.object);
        }
      })
    }

    const clip = (shape) => {
      store.dispatch("stage/shapeObject", {
        ...stream,
        shape,
      });
    };

    const localMuted = ref(false);
    const toggleMuted = () => {
      localMuted.value = !localMuted.value;
    };

    return {
      video,
      stream,
      loadeddata,
      clip,
      shapes,
      loading,
      localMuted,
      toggleMuted,
      isPlayer,
    };
  },
};
</script>

<style lang="scss" scoped>
.mute-icon {
  position: absolute;
  width: 24px;
  height: 20px;
  bottom: 8px;
  right: 8px;

  &:hover {
    transform: scale(1.2);
  }
}
</style>