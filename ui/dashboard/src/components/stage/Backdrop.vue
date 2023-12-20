<template>
  <Image
    class="background-image"
    :src="src"
    :style="{
      opacity: backgroundOpacity,
    }"
    :transition="transitionDuration"
    :no-fallback="true"
  />
</template>

<script>
import { computed, reactive } from "@vue/reactivity";
import { watch } from "@vue/runtime-core";
import { useStore } from "vuex";
import Image from "../Image.vue";

export default {
  components: { Image },
  setup: () => {
    const store = useStore()
    const background = computed(() => store.state.stage.background);
    const backgroundOpacity = computed(
      () => store.state.stage.background?.opacity ?? 1
    );
    const transitionDuration = computed(() => 100 / store.state.stage.background?.speed);

    const frameAnimation = reactive({
      interval: null,
      currentFrame: null,
    });
    const src = computed(() => {
      if (!background.value) {
        return null
      }
      if (background.value.multi && background.value.speed > 0) {
        return frameAnimation.currentFrame
      } else {
        return background.value.currentFrame ?? background.value.src
      }
    })

    watch(background, (value) => {
      if (!value) return;
      const { speed, frames, currentFrame } = value;
      if (currentFrame) {
        frameAnimation.currentFrame = currentFrame
      }
      clearInterval(frameAnimation.interval);
      frameAnimation.interval = setInterval(() => {
        let nextFrame = frames.indexOf(frameAnimation.currentFrame) + 1;
        if (nextFrame >= frames.length) {
          nextFrame = 0;
        }
        frameAnimation.currentFrame = frames[nextFrame];
      }, 100 / speed);
    }, { immediate: true });

    return { backgroundOpacity, transitionDuration, src }
  }
}
</script>

<style scoped>
.background-image {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: auto;
}
</style>