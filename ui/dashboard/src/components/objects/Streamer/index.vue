<template>
  <div>
    <Object :object="object">
      <template #menu="slotProps">
        <div class="avatar-context-menu card-content p-0">
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
      v-if="isHost"
      :src="stream.url"
      preload="auto"
      controls
      @play="handlePlay"
      style="display: none"
    ></video>
  </div>
</template>

<script>
import { computed, reactive, ref, watchEffect } from "vue";
import Object from "../Object.vue";
import { useStore } from "vuex";
import { cropImageFromCanvas } from "@/utils/canvas";
export default {
  components: { Object },
  props: ["stream"],
  setup: (props) => {
    const store = useStore();
    const object = reactive(props.stream);
    const video = ref();
    const canvas = document.createElement("canvas");
    const ctx = canvas.value.getContext("2d");

    watchEffect(() => {
      object.src =
        store.state.stage.board.streams[props.stream.id] ?? object.url;
    });

    const isHost = computed(() =>
      store.state.stage.hosts.some((stream) => stream.id === props.stream.id)
    );
    const handlePlay = (e) => {
      const $this = e.target;

      (function loop() {
        if (!$this.paused && !$this.ended) {
          ctx.drawImage($this, 0, 0);
          const { src } = cropImageFromCanvas(canvas);
          // store.dispatch("stage/sendStreamData", { id: props.stream.id, src });
          object.src = src;
          setTimeout(loop, 1000 / 30); // drawing at 30fps
        }
      })();
    };

    const playStream = ({ closeMenu }) => {
      video.value.play();
      object.isPlaying = true;
      closeMenu();
    };

    const pauseStream = ({ closeMenu }) => {
      video.value.pause();
      object.isPlaying = false;
      closeMenu();
    };

    const clipCircle = () => {};

    return {
      video,
      object,
      isHost,
      handlePlay,
      playStream,
      pauseStream,
      clipCircle,
    };
  },
};
</script>

<style>
</style>