<template>
  <div class="avatar-context-menu card-content p-0">
    <template v-if="holdable">
      <a v-if="isHolding" class="panel-block" @click.stop="releaseAvatar">
        <span class="panel-icon">
          <Icon src="clear.svg" />
        </span>
        <span>Release</span>
      </a>
      <a v-else class="panel-block" @click="holdAvatar">
        <span class="panel-icon">
          <Icon src="set-as-avatar.svg" />
        </span>
        <span>Hold this avatar</span>
      </a>
    </template>
    <template v-else>
      <a v-if="isWearing" class="panel-block" @click="takeOffCostume">
        <span class="panel-icon">
          <Icon src="clear.svg" />
        </span>
        <span>Remove from avatar</span>
      </a>
      <a v-else-if="currentAvatar" class="panel-block" @click="wearCostume">
        <span class="panel-icon">
          <Icon src="props.svg" />
        </span>
        <span>Add to avatar</span>
      </a>
    </template>
    <a class="panel-block" @click="bringToFront">
      <span class="panel-icon">
        <Icon src="bring-to-front.svg" />
      </span>
      <span>Bring forward</span>
    </a>
    <a class="panel-block" @click="sendToBack">
      <span class="panel-icon">
        <Icon src="send-to-back.svg" />
      </span>
      <span>Send back</span>
    </a>
    <a v-if="holdable" class="panel-block" @click="changeNickname">
      <span class="panel-icon">
        <Icon src="change-nickname.svg" />
      </span>
      <span>Avatar name</span>
    </a>
    <a v-if="holdable" class="panel-block" @click="openVoiceSetting">
      <span class="panel-icon">
        <Icon src="voice-setting.svg" />
      </span>
      <span>Voice setting</span>
    </a>
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
            'has-background-primary-light': sliderMode === 'opacity',
          }"
          @click="changeSliderMode('opacity')"
          data-tooltip="Opacity slider"
        >
          <span class="mt-1">
            <Icon src="opacity-slider.svg" />
          </span>
        </button>
      </p>
      <p class="control menu-group-item">
        <button
          class="button is-light"
          :class="{
            'has-background-warning-light': sliderMode === 'animation',
          }"
          @click="changeSliderMode('animation')"
          data-tooltip="Animation speed"
        >
          <span class="mt-1">
            <Icon src="animation-slider.svg" />
          </span>
        </button>
      </p>
      <p class="control menu-group-item">
        <button
          class="button is-light"
          :class="{
            'has-background-danger-light': sliderMode === 'speed',
          }"
          @click="changeSliderMode('speed')"
          data-tooltip="Move speed"
        >
          <span class="mt-1">
            <Icon src="movement-slider.svg" />
          </span>
        </button>
      </p>
    </div>
    <a class="panel-block has-text-danger" @click="deleteObject">
      <span class="panel-icon">
        <Icon src="remove.svg" />
      </span>
      <span>Remove</span>
    </a>
    <div v-if="object.multi" class="field has-addons menu-group">
      <p class="control menu-group-item" @click="toggleAutoplayFrames()">
        <button class="button is-light">
          <Icon :src="object.autoplayFrames > 0 ? 'pause.svg' : 'play.svg'" />
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
import { computed, inject, ref } from "vue";
import Icon from "@/components/Icon";

export default {
  props: [
    "object",
    "closeMenu",
    "active",
    "sliderMode",
    "setSliderMode",
    "keepActive",
  ],
  emits: ["update:active", "hold"],
  components: { Icon },
  setup: (props, { emit }) => {
    const store = useStore();

    const holdAvatar = () => {
      store.dispatch("user/setAvatarId", props.object.id).then(props.closeMenu);
    };

    const releaseAvatar = () => {
      store.dispatch("user/setAvatarId", null).then(props.closeMenu);
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
      store
        .dispatch("stage/openSettingPopup", {
          type: "ChatParameters",
        })
        .then(props.closeMenu);

    const bringToFront = () => {
      store.dispatch("stage/bringToFront", props.object).then(props.closeMenu);
    };

    const sendToBack = () => {
      store.dispatch("stage/sendToBack", props.object).then(props.closeMenu);
    };

    const changeSliderMode = (mode) => {
      props.setSliderMode(mode);
      emit("update:active", true);
      props.keepActive(true);
    };

    const holdable = inject("holdable") ?? ref();
    const isHolding = computed(
      () =>
        props.object.holder &&
        props.object.holder.id === store.state.stage.session
    );

    const openVoiceSetting = () => {
      store
        .dispatch("stage/openSettingPopup", {
          type: "VoiceParameters",
        })
        .then(props.closeMenu);
    };

    const isWearing = inject("isWearing");
    const currentAvatar = computed(() => store.getters["stage/currentAvatar"]);

    const wearCostume = () => {
      if (currentAvatar.value) {
        store
          .dispatch("stage/shapeObject", {
            ...props.object,
            wornBy: currentAvatar.value.id,
          })
          .then(props.closeMenu);
      }
    };

    const takeOffCostume = () => {
      if (isWearing.value) {
        store
          .dispatch("stage/shapeObject", {
            ...props.object,
            wornBy: null,
          })
          .then(props.closeMenu);
      }
    };

    return {
      switchFrame,
      holdAvatar,
      releaseAvatar,
      deleteObject,
      changeNickname,
      bringToFront,
      sendToBack,
      toggleAutoplayFrames,
      changeSliderMode,
      openVoiceSetting,
      wearCostume,
      takeOffCostume,
      currentAvatar,
      isWearing,
      isHolding,
      holdable,
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