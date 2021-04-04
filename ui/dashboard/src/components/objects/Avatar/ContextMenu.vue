<template>
  <div class="avatar-context-menu card-content p-0">
    <a
      v-if="object.type !== 'prop'"
      class="panel-block"
      @click="setAsPrimaryAvatar"
    >
      <span class="panel-icon">
        <Icon src="set-as-avatar.svg" />
      </span>
      <span>Set as your avatar</span>
    </a>
    <a class="panel-block" @click="bringToFront">
      <span class="panel-icon">
        <Icon src="bring-to-front.svg" />
      </span>
      <span>Bring to front</span>
    </a>
    <a class="panel-block" @click="sendToBack">
      <span class="panel-icon">
        <Icon src="send-to-back.svg" />
      </span>
      <span>Send to back</span>
    </a>
    <a
      v-if="object.type !== 'prop'"
      class="panel-block"
      @click="changeNickname"
    >
      <span class="panel-icon">
        <Icon src="change-nickname.svg" />
      </span>
      <span>Change your nickname</span>
    </a>
    <div class="field has-addons menu-group">
      <p class="control menu-group-title">
        <span class="panel-icon pt-1">
          <Icon src="rotation-slider.svg" />
        </span>
        <span>Rotation</span>
      </p>
      <p class="control menu-group-item">
        <button class="button is-light" @click="rotate(+45)">
          <span class="panel-icon">
            <Icon src="45degpositive.svg" />
          </span>
          <span>+ 45deg</span>
        </button>
      </p>
      <p class="control menu-group-item">
        <button class="button is-light" @click="rotate(-45)">
          <span class="panel-icon">
            <Icon src="45degnegative.svg" />
          </span>
          <span>- 45deg</span>
        </button>
      </p>
    </div>
    <div class="field has-addons menu-group">
      <p class="control menu-group-title">
        <span class="panel-icon pt-1">
          <Icon src="rotation-slider.svg" />
        </span>
        <span>Slider</span>
      </p>
      <p class="control menu-group-item">
        <button
          class="button is-light"
          :class="{
            'has-background-primary has-text-white': sliderMode === 'opacity',
          }"
          @click="changeSliderMode('opacity')"
        >
          <span>Opacity</span>
        </button>
      </p>
      <p class="control menu-group-item">
        <button
          class="button is-light"
          :class="{
            'has-background-warning': sliderMode === 'animation',
          }"
          @click="changeSliderMode('animation')"
        >
          <span>Frame Animation</span>
        </button>
      </p>
      <p class="control menu-group-item">
        <button
          class="button is-light"
          :class="{
            'has-background-danger has-text-white': sliderMode === 'speed',
          }"
          @click="changeSliderMode('speed')"
        >
          <span>Move Speed</span>
        </button>
      </p>
    </div>
    <a class="panel-block has-text-danger" @click="deleteObject">
      <span class="panel-icon">
        <Icon src="delete.svg" />
      </span>
      <span>Delete</span>
    </a>
    <div v-if="object.multi" class="field has-addons menu-group">
      <p class="control menu-group-item" @click="toggleAutoplayFrames()">
        <button class="button is-light">
          <i v-if="object.autoplayFrames" class="fas fa-3x fa-pause"></i>
          <Icon v-else src="play.svg" />
        </button>
      </p>
      <p
        v-for="frame in object.frames"
        :key="frame"
        @click="switchFrame(frame)"
        class="control menu-group-item"
      >
        <button class="button is-light">
          <img :src="frame" style="height: 100%" />
        </button>
      </p>
    </div>
  </div>
</template>

<script>
import { useStore } from "vuex";
import { computed } from "vue";
import Icon from "@/components/Icon";

export default {
  props: ["object", "closeMenu", "active"],
  emits: ["update:active", "hold"],
  components: { Icon },
  setup: (props, { emit }) => {
    const store = useStore();

    const setAsPrimaryAvatar = () => {
      emit("hold");
    };

    const deleteObject = () => {
      store.dispatch("stage/deleteObject", props.object).then(props.closeMenu);
    };

    const switchFrame = (frame) => {
      store.dispatch("stage/switchFrame", {
        ...props.object,
        src: frame,
      });
    };

    const toggleAutoplayFrames = () => {
      store
        .dispatch("stage/toggleAutoplayFrames", {
          ...props.object,
          autoplayFrames: props.object.autoplayFrames ? 0 : 100,
        })
        .then(() => {
          emit("update:active", true);
        });
    };

    const changeNickname = () =>
      store.dispatch("stage/openSettingPopup", {
        type: "Chat",
      });

    const bringToFront = () => {
      store.dispatch("stage/bringToFront", props.object).then(props.closeMenu);
    };

    const sendToBack = () => {
      store.dispatch("stage/sendToBack", props.object).then(props.closeMenu);
    };

    const sliderMode = computed(() => store.state.stage.preferences.slider);
    const changeSliderMode = (mode) => {
      store.dispatch("stage/changeSliderMode", mode).then(() => {
        emit("update:active", true);
      });
    };

    const rotate = (deg) => {
      store.dispatch("stage/shapeObject", {
        ...props.object,
        rotate: (props.object.rotate ?? 0) + deg,
      });
    };

    return {
      switchFrame,
      setAsPrimaryAvatar,
      deleteObject,
      changeNickname,
      bringToFront,
      sendToBack,
      toggleAutoplayFrames,
      sliderMode,
      changeSliderMode,
      rotate,
    };
  },
};
</script>

<style scoped lang="scss">
@import "@/styles/bulma";
@import "@/styles/mixins";

.avatar-context-menu {
  * {
    font-size: 14px;
  }
  .panel-block {
    &:hover {
      z-index: 100;
      position: relative;
      font-size: 14px;
    }
  }
  .menu-group {
    width: 100%;
    display: flex;
    margin-bottom: 0;
    .menu-group-title {
      flex: none;
      padding: 6px 12px;
      width: 100px;
      white-space: nowrap;
      > button {
        justify-content: start;
        padding-left: 12px;
      }
    }
    .menu-group-item {
      flex: auto;
    }
    button {
      width: 100%;
    }
  }
}
</style>