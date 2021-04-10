<template>
  <div
    class="avatar-topping"
    :style="{
      top: position.y - 26 + 'px',
      left: position.x + position.w / 2 + 'px',
    }"
  >
    <span
      v-if="holder && isPlayer"
      class="icon marker"
      :class="{ inactive: !active }"
      :data-tooltip="`${object.name ? object.name + ' held by' : 'Held by'} ${
        holder.nickname
      }`"
    >
      <Icon src="my-avatar.svg" />
    </span>
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
import { computed, inject } from "vue";
import { useStore } from "vuex";
import anime from "animejs";
import Icon from "@/components/Icon";
export default {
  props: ["position", "object"],
  components: { Icon },
  setup: (props) => {
    const store = useStore();
    const holder = inject("holder");
    const active = computed(
      () => props.object.id === store.state.user.avatarId
    );
    const isPlayer = computed(() => store.getters["auth/loggedIn"]);

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

    return { active, enter, leave, holder, isPlayer };
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
  left: -10px;
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
.inactive {
  filter: grayscale(1);
}
</style>