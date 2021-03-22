<template>
  <div
    class="avatar-topping"
    :style="{
      top: position.y - 26 + 'px',
      left: position.x + position.w / 2 + 'px',
    }"
  >
    <div
      v-show="active"
      :style="{
        position: 'absolute',
        width: '100px',
        left: position.w / 2 - 96 + 'px',
      }"
      @mousedown.stop="keepActive"
      @mouseover.stop="keepActive"
      @mouseup.stop="keepActive"
    >
      <button class="button is-rounded is-small">
        <i class="fas fa-border-none"></i>
      </button>
      <button
        class="button is-rounded is-small"
        :class="{ 'is-primary': object.liveAction }"
        @click="toggleLiveAction"
      >
        <i class="fas fa-lightbulb"></i>
      </button>
      <button class="button is-rounded is-small" @click="deleteObject">
        <i class="fas fa-times"></i>
      </button>
    </div>
    <i
      v-show="chosen"
      class="marker fas fa-map-marker-alt fa-lg has-text-warning"
    ></i>
    <transition @enter="enter" @leave="leave" :css="false" appear>
      <div
        v-if="object.speak"
        class="chat-bubble"
        tabindex="-1"
        :key="object.speak"
        :style="{
          'max-width': position.w + 'px',
          'min-width': position.w < 100 ? '100px' : 'unset',
        }"
      >
        <span>{{ object.speak.message }}</span>
        <i class="fas fa-caret-down"></i>
      </div>
    </transition>
  </div>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import anime from "animejs";
export default {
  props: ["position", "object", "active"],
  emits: ["update:active"],
  setup: (props, { emit }) => {
    const store = useStore();
    const chosen = computed(
      () => props.object.id === store.state.user.avatarId
    );

    const enter = (el, complete) => {
      anime({
        targets: el,
        scale: [0, 1],
        rotate: [180, 0],
        translateY: [0, "-100%"],
        translateX: [0, "-50%"],
        complete,
      });
    };

    const leave = (el, complete) => {
      anime({
        targets: el,
        scale: [1, 0],
        rotate: [0, 180],
        complete,
      });
    };

    const keepActive = () => {
      emit("update:active", true);
    };

    const toggleLiveAction = () => {
      store.dispatch("stage/shapeObject", {
        ...props.object,
        liveAction: !props.object.liveAction,
      });
    };

    const deleteObject = () => {
      store.dispatch("stage/deleteObject", props.object);
    };

    return { chosen, enter, leave, deleteObject, keepActive, toggleLiveAction };
  },
};
</script>

<style scoped lang="scss">
.avatar-topping {
  position: fixed;
}
.chat-bubble {
  position: fixed;
  border-radius: 4px;
  padding: 0.25em 0.75em;
  text-align: center;
  line-height: 1em;
  background: white;
  box-shadow: 0 0.5em 1em -0.125em rgba(10, 10, 10, 0.1),
    0 0px 0 1px rgba(10, 10, 10, 0.02);
  i.fas {
    position: absolute;
    left: calc(50% - 4px);
    bottom: -8px;
    color: white;
  }
}
.marker {
  position: absolute;
  left: -8px;
  -webkit-animation: spin 2s linear infinite;
  -moz-animation: spin 2s linear infinite;
  animation: spin 2s linear infinite;
}
@-moz-keyframes spin {
  100% {
    -moz-transform: rotate3d(0, 1, 0, 360deg);
  }
}
@-webkit-keyframes spin {
  100% {
    -webkit-transform: rotate3d(0, 1, 0, 360deg);
  }
}
@keyframes spin {
  100% {
    -webkit-transform: rotate3d(0, 1, 0, 360deg);
    transform: rotate3d(0, 1, 0, 360deg);
  }
}
</style>