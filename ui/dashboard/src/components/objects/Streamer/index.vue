<template>
  <div>
    <Object :object="stream">
      <template #menu="slotProps">
        <MenuContent :object="object" :stream="stream" v-bind="slotProps" v-model:active="active" />
      </template>

      <template #render>
        <Loading v-if="loading" height="100%" />
        <video
          v-bind:id="'video' + stream.id"
          v-show="!loading"
          ref="video"
          :src="object.url"
          :muted="localMuted"
          preload="auto"
          disablePictureInPicture
          @loadeddata="loadeddata"
          @ended="stream.isPlaying = false"
          :style="{
            'border-radius': stream.shape === 'circle' ? '100%' : 0,
          }"
        ></video>
        <button class="button is-small mute-icon clickable" @mousedown="toggleMuted">
          <i v-if="localMuted" class="fas fa-volume-mute has-text-danger"></i>
          <i v-else class="fas fa-volume-up has-text-primary"></i>
        </button>
      </template>
    </Object>
  </div>
</template>

<script>
import { computed, onMounted, reactive, ref, watch } from "vue";
import Object from "../Object.vue";
import { useStore } from "vuex";
import { useFlv } from "./composable";
import { getSubsribeLink } from "@/utils/streaming";
import Loading from "@/components/Loading.vue";
import { nmsService } from "@/services/rest";
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
      useFlv(video, fullUrl);
    }


    const clip = (shape) => {
      store.dispatch("stage/shapeObject", {
        ...stream,
        shape,
      });
    };

    const localMuted = ref(true);
    const toggleMuted = () => {
      localMuted.value = !localMuted.value;
    };

    onMounted(async () => {
      const streams = await nmsService.getStreams();
      if (!streams.some((s) => s.url === props.object.url)) {
        // Delete stream because it is not running anymore
        store.dispatch("stage/deleteObject", props.object);
      }
    });

    return {
      video,
      stream,
      loadeddata,
      clip,
      shapes,
      loading,
      localMuted,
      toggleMuted,
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