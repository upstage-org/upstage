<template>
  <div
    class="avatar-topping"
    :style="{
      top: position.y - 26 + 'px',
      left: position.x + position.w / 2 + 'px',
    }"
  >
    <i
      v-show="active"
      class="marker fas fa-map-marker-alt fa-lg has-text-warning"
    ></i>
    <transition @enter="enter" @leave="leave" :css="false">
      <div
        v-if="object.speak"
        class="chat-bubble tag is-medium"
        :key="object.speak"
        :style="{
          'background-color': object.speak.backgroundColor,
          color: object.speak.color,
        }"
      >
        <span>{{ object.speak.message }}</span>
        <i
          class="fas fa-caret-down"
          :style="{
            color: object.speak.backgroundColor,
          }"
        ></i>
      </div>
    </transition>
  </div>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import anime from "animejs";
export default {
  props: ["position", "object"],
  setup: (props) => {
    const store = useStore();
    const active = computed(
      () => props.object.id === store.state.user.avatarId
    );

    const enter = (el, complete) => {
      anime({
        targets: el,
        scale: [0, 1],
        rotate: [180, 0],
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

    return { active, enter, leave };
  },
};
</script>

<style scoped lang="scss">
.avatar-topping {
  position: fixed;
}
.chat-bubble {
  position: relative;
  top: -15px;
  left: -50%;
  i.fas {
    position: absolute;
    top: 25px;
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