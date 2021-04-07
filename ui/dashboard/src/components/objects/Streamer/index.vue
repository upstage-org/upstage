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
                  <i class="fas fa-ban"></i>
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
            <p class="control menu-group-item" @click="clip(vue)">
              <button class="button is-light">
                <img style="height: 100%" :src="vue" />
              </button>
            </p>
            <p class="control menu-group-item" @click="clip(dog)">
              <button class="button is-light">
                <img style="height: 100%" :src="dog" />
              </button>
            </p>
          </div>
        </div>
      </template>
    </Object>
    <video
      ref="video"
      :src="object.url"
      preload="auto"
      :muted="!isHost"
      @loadeddata="loadeddata"
      @ended="stream.isPlaying = false"
      style="display: none"
    ></video>
  </div>
</template>

<script>
import { computed, reactive, ref, watch } from "vue";
import Object from "../Object.vue";
import { useStore } from "vuex";
import { useShape } from "./composable";
import vue from "@/assets/logo.png";
import dog from "@/assets/dog.png";

export default {
  components: { Object },
  props: ["object"],
  setup: (props) => {
    const store = useStore();
    const stream = reactive({ ...props.object, isPlaying: true });
    const video = ref();

    const isHost = computed(() =>
      store.state.stage.hosts.some((object) => object.id === props.object.id)
    );

    const synchronize = () => {
      if (stream.isPlaying) {
        video.value.play();
      } else {
        video.value.pause();
      }
    };

    watch(props.object, () => {
      delete props.object.src;
      window.Object.assign(stream, props.object);
      synchronize();
    });

    const loadeddata = () => {
      synchronize();
    };

    const { src } = useShape(video, stream);
    watch(src, () => (stream.src = src.value));

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
      isHost,
      loadeddata,
      playStream,
      pauseStream,
      clip,
      vue,
      dog,
    };
  },
};
</script>

<style>
</style>