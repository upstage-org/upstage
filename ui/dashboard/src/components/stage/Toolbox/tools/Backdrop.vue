<template>
  <div @click="setBackground({ src: null })">
    <div class="icon is-large"><Icon size="36" src="clear.svg" /></div>
    <span class="tag is-light is-block">Clear</span>
  </div>
  <div
    v-for="background in backgrounds"
    :key="background"
    :class="{
      active: background.id === currentBackground.id,
      flex: !(background.multi && background.id === currentBackground.id),
    }"
  >
    <ContextMenu>
      <template #trigger>
        <Image :src="background.src" @click="setBackground(background)" />
        <template v-if="background.multi">
          <div v-if="background.id === currentBackground.id">
            <input
              class="slider is-fullwidth is-primary mt-0"
              step="0.01"
              min="0"
              max="1"
              :value="currentBackground.speed ?? 0"
              @change="changeBackdropSpeed"
              type="range"
            />
          </div>
          <Icon
            v-else
            class="is-multi"
            title="This is a multiframe backdrop"
            src="multi-frame.svg"
          />
        </template>
      </template>
      <template #context>
        <div
          v-if="background.multi && background.id === currentBackground.id"
          class="field has-addons menu-group"
        >
          <p class="control menu-group-item" @click="toggleAutoplayFrames()">
            <button class="button is-light">
              <Icon
                :src="currentBackground.speed > 0 ? 'pause.svg' : 'play.svg'"
              />
            </button>
          </p>
          <p
            v-for="frame in background.frames"
            :key="frame"
            @click="switchBackdropFrame(frame)"
            class="control menu-group-item"
          >
            <button class="button is-light">
              <img :src="frame" style="height: 100%" />
            </button>
          </p>
        </div>
      </template>
    </ContextMenu>
  </div>
</template>

<script>
import { useStore } from "vuex";
import { computed } from "vue";
import Image from "@/components/Image";
import Icon from "@/components/Icon";
import ContextMenu from "@/components/ContextMenu";

export default {
  components: { Image, Icon, ContextMenu },
  setup: () => {
    const store = useStore();
    const currentBackground = computed(() => store.state.stage.background);

    const backgrounds = computed(() => store.state.stage.tools.backdrops);

    const setBackground = (background) => {
      store.dispatch("stage/setBackground", background);
    };

    const changeBackdropSpeed = (e) => {
      store.dispatch("stage/setBackground", {
        ...currentBackground.value,
        speed: e.target.value,
      });
    };

    const toggleAutoplayFrames = () => {
      let speed = 0;
      if (!currentBackground.value.speed) {
        speed = 0.5;
      }
      store.dispatch("stage/setBackground", {
        ...currentBackground.value,
        speed,
      });
    };

    const switchBackdropFrame = (currentFrame) => {
      store.dispatch("stage/setBackground", {
        ...currentBackground.value,
        currentFrame,
      });
    };

    return {
      backgrounds,
      setBackground,
      currentBackground,
      changeBackdropSpeed,
      toggleAutoplayFrames,
      switchBackdropFrame,
    };
  },
};
</script>

<style scoped>
.flex {
  display: flex;
}
</style>