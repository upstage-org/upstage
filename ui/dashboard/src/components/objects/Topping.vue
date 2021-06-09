<template>
  <teleport to="body">
    <div
      class="avatar-topping"
      :style="{
        left: stageSize.left + object.x + object.w / 2 + 'px',
        top: stageSize.top + object.y - 30 + 'px',
      }"
      @click="openChatBox"
    >
      <span
        v-if="object.holder && canPlay"
        class="icon marker"
        :class="{ inactive: !isHolding }"
        :data-tooltip="`${object.name ? object.name + ' held by' : 'Held by'} ${
          object.holder.nickname
        }`"
      >
        <Icon src="my-avatar.svg" />
      </span>
      <transition @enter="enter" @leave="leave" :css="false" appear>
        <blockquote
          v-if="object.speak"
          class="bubble"
          tabindex="-1"
          :key="object.speak"
          :class="object.speak.behavior ?? 'speak'"
        >
          <div class="py-2 px-4">
            <Linkify>{{ object.speak.message }}</Linkify>
          </div>
        </blockquote>
      </transition>
    </div>
  </teleport>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import anime from "animejs";
import Icon from "@/components/Icon";
import Linkify from "@/components/Linkify";
export default {
  props: ["object", "active"],
  components: { Icon, Linkify },
  setup: (props) => {
    const store = useStore();
    const isHolding = computed(
      () => props.object.id === store.state.user.avatarId
    );
    const canPlay = computed(() => store.getters["stage/canPlay"]);

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

    const openChatBox = () => {
      if (isHolding.value) {
        store.dispatch("stage/openSettingPopup", {
          type: "ChatBox",
          simple: true,
        });
      }
    };
    const stageSize = computed(() => store.getters["stage/stageSize"]);

    return {
      enter,
      leave,
      isHolding,
      canPlay,
      openChatBox,
      stageSize,
      max: Math.max,
    };
  },
};
</script>

<style scoped lang="scss">
.avatar-topping {
  position: fixed;
  z-index: 3000;
}
.marker {
  position: absolute;
  left: -12px;
}
.inactive {
  filter: grayscale(1);
}
</style>