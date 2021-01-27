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
    <a class="panel-block p-0">
      <div class="field has-addons menu-group">
        <p class="control menu-group-title">
          <button class="button is-white">
            <span class="panel-icon">
              <i class="fas fa-sliders-h has-text-info"></i>
            </span>
            <span>Rotation</span>
          </button>
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
    </a>
    <a class="panel-block p-0">
      <div class="field has-addons menu-group">
        <p class="control menu-group-title">
          <button class="button is-white" style="padding-left: 12px">
            <span class="panel-icon">
              <i class="fas fa-sliders-h has-text-info"></i>
            </span>
            <span>Slider</span>
          </button>
        </p>
        <p class="control menu-group-item">
          <button
            class="button is-light"
            :class="{ 'is-primary': sliderMode === 'opacity' }"
            @click="changeSliderMode('opacity')"
          >
            <span>Opacity</span>
          </button>
        </p>
        <p class="control menu-group-item">
          <button
            class="button is-light"
            :class="{ 'is-warning': sliderMode === 'animation' }"
            @click="changeSliderMode('animation')"
          >
            <span>Frame Animation</span>
          </button>
        </p>
        <p class="control menu-group-item">
          <button
            class="button is-light"
            :class="{ 'is-danger': sliderMode === 'speed' }"
            @click="changeSliderMode('speed')"
          >
            <span>Move Speed</span>
          </button>
        </p>
      </div>
    </a>
    <a class="panel-block has-text-danger" @click="deleteObject">
      <span class="panel-icon">
        <i class="fas fa-trash has-text-danger"></i>
      </span>
      <span>Delete</span>
    </a>
    <a v-if="object.multi" class="panel-block">
      <div class="columns is-vcentered frame-selector is-multiline">
        <div class="column is-3" @click="toggleAutoplayFrames">
          <div class="icon is-large autoplay-frames">
            <i
              class="fas fa-3x"
              :class="{
                'fa-play': !object.autoplayFrames,
                'fa-pause': object.autoplayFrames,
              }"
            ></i>
          </div>
        </div>
        <div
          v-for="frame in object.frames"
          :key="frame"
          class="column is-3"
          @click="switchFrame(frame)"
        >
          <Image :src="frame" />
        </div>
      </div>
    </a>
  </div>
</template>

<script>
import { useStore } from "vuex";
import Image from "@/components/Image";
import { computed } from "vue";

export default {
  props: ["object", "closeMenu", "active"],
  emits: ["update:active"],
  components: { Image },
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
.avatar-context-menu {
  font-size: 14px;
  .button {
    font-size: 14px;
  }
  .menu-group {
    width: 100%;
    display: flex;
    .menu-group-title {
      flex: none;
      width: 100px;
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