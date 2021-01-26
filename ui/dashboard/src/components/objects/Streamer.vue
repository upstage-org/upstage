<template>
  <div>
    <Object :object="object">
      <template #menu="slotProps">
        <div class="avatar-context-menu card-content p-0">
          <a class="panel-block has-text-info" @click="slotProps.closeMenu()">
            <span class="panel-icon">
              <i class="fas fa-map-marker-alt has-text-info"></i>
            </span>
            <span>Change Shape</span>
          </a>
        </div>
      </template>
    </Object>
    <video
      v-if="isHost"
      :src="stream.url"
      preload="auto"
      controls
      @loadeddata="handleLoad"
      @play="handlePlay"
    ></video>
  </div>
</template>

<script>
import { computed, reactive, watchEffect } from "vue";
import Object from "./Object.vue";
import { useStore } from "vuex";
import { cropImageFromCanvas } from "@/utils/canvas";
export default {
  components: { Object },
  props: ["stream"],
  setup: (props) => {
    const store = useStore();
    const object = reactive(props.stream);

    watchEffect(() => {
      object.src = store.state.stage.board.streams[props.stream.id];
    });

    const isHost = computed(() =>
      store.state.stage.hosts.some((stream) => stream.id === props.stream.id)
    );
    const handlePlay = (e) => {
      const $this = e.target;
      const $canvas = document.createElement("canvas");
      const ctx = $canvas.getContext("2d");

      (function loop() {
        if (!$this.paused && !$this.ended) {
          ctx.drawImage($this, 0, 0);
          const { src } = cropImageFromCanvas($canvas);
          // store.dispatch("stage/sendStreamData", { id: props.stream.id, src });
          object.src = src;
          setTimeout(loop, 1000 / 30); // drawing at 30fps
        }
      })();
    };

    return { object, isHost, handlePlay };
  },
};
</script>

<style>
</style>