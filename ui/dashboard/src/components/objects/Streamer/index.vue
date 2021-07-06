<template>
  <div>
    <Object :object="stream">
      <template #menu="slotProps">
        <div class="avatar-context-menu card-content p-0">
          <a
            v-if="stream.isPlaying"
            class="panel-block has-text-info"
            @click="pauseStream(slotProps)"
          >
            <span class="panel-icon">
              <i class="fas fa-pause"></i>
            </span>
            <span>Pause</span>
          </a>
          <a
            v-else
            class="panel-block has-text-info"
            @click="playStream(slotProps)"
          >
            <span class="panel-icon">
              <i class="fas fa-play"></i>
            </span>
            <span>Play</span>
          </a>

          <div class="field has-addons menu-group">
            <p class="control menu-group-item">
              <button class="button is-light" @click="clip(null)">
                <div class="icon">
                  <i class="fas fa-square"></i>
                </div>
              </button>
            </p>
            <p class="control menu-group-item" @click="clip('circle')">
              <button class="button is-light">
                <div class="icon">
                  <i class="fas fa-circle"></i>
                </div>
              </button>
            </p>
          </div>
        </div>
      </template>
      <template #render>
        <Loading v-if="loading" height="100%" />
        <video
          v-show="!loading"
          ref="video"
          :src="object.url"
          preload="auto"
          @loadeddata="loadeddata"
          @ended="stream.isPlaying = false"
          :style="{
            'border-radius': stream.shape === 'circle' ? '100%' : 0,
          }"
        ></video>
      </template>
    </Object>
  </div>
</template>

<script>
import { computed, reactive, ref, watch } from "vue";
import Object from "../Object.vue";
import { useStore } from "vuex";
import { useFlv } from "./composable";
import { getSubsribeLink } from "@/utils/streaming";
import Loading from "@/components/Loading.vue";

export default {
  components: { Object, Loading },
  props: ["object"],
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

    const playStream = ({ closeMenu }) => {
      store
        .dispatch("stage/shapeObject", {
          ...stream,
          isPlaying: true,
        })
        .then(closeMenu);
    };

    const pauseStream = ({ closeMenu }) => {
      store
        .dispatch("stage/shapeObject", {
          ...stream,
          isPlaying: false,
        })
        .then(closeMenu);
    };

    const clip = (shape) => {
      store.dispatch("stage/shapeObject", {
        ...stream,
        shape,
      });
    };

    return {
      video,
      stream,
      loadeddata,
      playStream,
      pauseStream,
      clip,
      shapes,
      loading,
    };
  },
};
</script>

<style>
</style>