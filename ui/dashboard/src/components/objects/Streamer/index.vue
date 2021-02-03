<template>
  <div>
    <Object :object="object">
      <template #menu="slotProps">
        <div v-if="isHost" class="avatar-context-menu card-content p-0">
          <a
            v-if="object.isPlaying"
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
          <a class="panel-block">
            <div class="columns is-vcentered frame-selector is-multiline">
              <div class="column is-3" @click="clipCircle">
                <div class="icon is-large autoplay-frames">
                  <i class="fas fa-3x fa-circle"></i>
                </div>
              </div>
            </div>
          </a>
        </div>
      </template>
    </Object>
    <video
      ref="video"
      :src="stream.url"
      preload="auto"
      :muted="!isHost"
      @ended="object.isPlaying = false"
      style="display: none"
    ></video>
  </div>
</template>

<script>
import { computed, reactive, ref, watch } from "vue";
import Object from "../Object.vue";
import { useStore } from "vuex";
import { useShape } from "./composable";

export default {
  components: { Object },
  props: ["stream"],
  setup: (props) => {
    const store = useStore();
    const object = reactive({ ...props.stream });
    const video = ref();

    const isHost = computed(() =>
      store.state.stage.hosts.some((stream) => stream.id === props.stream.id)
    );

    watch(props.stream, () => {
      if (props.stream.isPlaying) {
        video.value.play();
      } else {
        video.value.pause();
      }
      window.Object.assign(object, props.stream);
    });

    const { src } = useShape(video, object);
    watch(src, () => (object.src = src.value));

    const playStream = ({ closeMenu }) => {
      store
        .dispatch("stage/shapeObject", {
          ...object,
          isPlaying: true,
        })
        .then(closeMenu);
    };

    const pauseStream = ({ closeMenu }) => {
      store
        .dispatch("stage/shapeObject", {
          ...object,
          isPlaying: false,
        })
        .then(closeMenu);
    };

    const clipCircle = () => {
      store.dispatch("stage/shapeObject", {
        ...object,
        shape: "circle",
      });
    };

    return {
      video,
      object,
      isHost,
      playStream,
      pauseStream,
      clipCircle,
    };
  },
};
</script>

<style>
</style>