<template>
  <div
    ref="el"
    tabindex="0"
    @keyup.delete="deleteObject"
    @dblclick="hold"
    :style="
      activeMovable
        ? {
            position: 'relative',
            'z-index': 1,
          }
        : {}
    "
  >
    <ContextMenu
      :pad-left="-stageSize.left"
      :pad-top="-stageSize.top"
      :pad-right="250"
      opacity="0.8"
    >
      <template #trigger>
        <div
          :style="{
            position: 'absolute',
            left: object.x + 'px',
            top: object.y + 'px',
            width: object.w + 'px',
            height: object.h + 'px',
            transform: `rotate(${object.rotate}deg)`,
          }"
        >
          <OpacitySlider
            v-model:active="active"
            v-model:slider-mode="sliderMode"
            :object="object"
          />
          <QuickAction :object="object" v-model:active="active" />
          <Topping :object="object" v-model:active="active" />
        </div>
        <Moveable
          v-model:active="active"
          :controlable="controlable"
          :object="object"
        >
          <div
            class="object"
            :style="{
              width: '100%',
              height: '100%',
              cursor: 'grab',
            }"
            @dragstart.prevent
          >
            <slot name="render">
              <Image class="the-object" :src="src" />
            </slot>
          </div>
        </Moveable>
      </template>
      <template #context="slotProps" v-if="controlable || isWearing">
        <slot
          name="menu"
          v-bind="slotProps"
          :slider-mode="sliderMode"
          :set-slider-mode="(mode) => (sliderMode = mode)"
          :keep-active="() => (active = true)"
        />
      </template>
    </ContextMenu>
  </div>
</template>

<script>
import { useStore } from "vuex";
import { computed, provide, reactive, ref, watch } from "vue";
import Image from "@/components/Image";
import ContextMenu from "@/components/ContextMenu";
import OpacitySlider from "./OpacitySlider";
import QuickAction from "./QuickAction";
import Topping from "./Topping.vue";
import Moveable from "./Moveable";

export default {
  props: ["object"],
  emits: ["dblclick"],
  components: {
    Image,
    ContextMenu,
    OpacitySlider,
    QuickAction,
    Topping,
    Moveable,
  },
  setup(props) {
    // Dom refs
    const el = ref();

    // Vuex store
    const store = useStore();
    const stageSize = computed(() => store.getters["stage/stageSize"]);

    // Local state
    const active = ref(false);
    const sliderMode = ref("opacity");
    const beforeDragPosition = ref();
    const isHolding = computed(
      () => props.object.holder?.id === store.state.stage.session
    );
    const holdable = computed(() =>
      ["avatar", "drawing"].includes(props.object.type)
    );
    const canPlay = computed(() => store.getters["stage/canPlay"]);
    const controlable = computed(() => {
      return holdable.value
        ? isHolding.value
        : canPlay.value && !props.object.wornBy;
    });
    provide("holdable", holdable);

    const deleteObject = () => {
      if (controlable.value) {
        store.dispatch("stage/deleteObject", props.object);
      }
    };

    const frameAnimation = reactive({
      interval: null,
      currentFrame: null,
    });
    if (props.object.multi) {
      watch(
        () => props.object.autoplayFrames,
        () => {
          const { autoplayFrames, frames, src } = props.object;
          clearInterval(frameAnimation.interval);
          if (autoplayFrames) {
            frameAnimation.currentFrame = src;
            frameAnimation.interval = setInterval(() => {
              let nextFrame = frames.indexOf(frameAnimation.currentFrame) + 1;
              if (nextFrame >= frames.length) {
                nextFrame = 0;
              }
              frameAnimation.currentFrame = frames[nextFrame];
            }, autoplayFrames);
          }
        },
        {
          immediate: true,
        }
      );
    }
    const src = computed(() => {
      if (props.object.autoplayFrames && props.object.multi) {
        return frameAnimation.currentFrame;
      } else {
        return props.object.src;
      }
    });

    const hold = () => {
      if (holdable.value && canPlay.value && !props.object.holder) {
        store.dispatch("user/setAvatarId", props.object.id);
      }
    };
    const activeMovable = computed(
      () => store.state.stage.activeMovable === props.object.id
    );

    const isWearing = computed(
      () => store.getters["stage/currentAvatar"]?.id === props.object.wornBy
    );
    provide("isWearing", isWearing);

    return {
      el,
      print,
      active,
      beforeDragPosition,
      deleteObject,
      src,
      stageSize,
      hold,
      isHolding,
      holdable,
      controlable,
      sliderMode,
      activeMovable,
      isWearing,
    };
  },
};
</script>

<style lang="scss">
@import "@/styles/bulma";
@import "@/styles/mixins";

div[tabindex] {
  outline: none;
}
.object {
  z-index: 10;
}
</style>