<template>
  <div class="avatar-context-menu card-content p-0">
    <a
      v-if="object.type !== 'prop'"
      class="panel-block has-text-info"
      @click="setAsPrimaryAvatar"
    >
      <span class="panel-icon">
        <i class="fas fa-map-marker-alt has-text-info"></i>
      </span>
      <span>Set as your avatar</span>
    </a>
    <a class="panel-block has-text-info" @click="bringToFront">
      <span class="panel-icon">
        <i class="fas fa-angle-double-up has-text-info"></i>
      </span>
      <span>Bring to front</span>
    </a>
    <a class="panel-block has-text-info" @click="sendToBack">
      <span class="panel-icon">
        <i class="fas fa-angle-double-down has-text-info"></i>
      </span>
      <span>Send to back</span>
    </a>
    <a
      v-if="object.type !== 'prop'"
      class="panel-block has-text-info"
      @click="changeNickname"
    >
      <span class="panel-icon">
        <i class="fas fa-comment-alt has-text-info"></i>
      </span>
      <span>Change your nickname</span>
    </a>
    <div class="field has-addons menu-group">
      <p class="control menu-group-title">
        <span class="panel-icon pt-1">
          <i class="fas fa-sliders-h has-text-info"></i>
        </span>
        <span class="has-text-info">Rotation</span>
      </p>
      <p class="control menu-group-item">
        <button class="button is-light" @click="rotate(+45)">
          <span class="panel-icon">
            <i class="fas fa-redo"></i>
          </span>
          <span>+ 45deg</span>
        </button>
      </p>
      <p class="control menu-group-item">
        <button class="button is-light" @click="rotate(-45)">
          <span class="panel-icon">
            <i class="fas fa-undo"></i>
          </span>
          <span>- 45deg</span>
        </button>
      </p>
    </div>
    <div class="field has-addons menu-group">
      <p class="control menu-group-title">
        <span class="panel-icon pt-1">
          <i class="fas fa-sliders-h has-text-info"></i>
        </span>
        <span class="has-text-info">Slider</span>
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
        <i class="fas fa-trash has-text-danger"></i>
      </span>
      <span>Delete</span>
    </a>
    <div v-if="object.multi" class="field has-addons menu-group">
      <p class="control menu-group-item" @click="toggleAutoplayFrames()">
        <button class="button is-light">
          <i
            class="fas fa-3x"
            :class="{
              'fa-play': !object.autoplayFrames,
              'fa-pause': object.autoplayFrames,
            }"
          ></i>
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

export default {
  props: ["object", "closeMenu", "active"],
  emits: ["update:active"],
  setup: (props, { emit }) => {
    const store = useStore();

    const setAsPrimaryAvatar = () => {
      const { name, id } = props.object;
      store.dispatch("user/setAvatarId", { id, name }).then(props.closeMenu);
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