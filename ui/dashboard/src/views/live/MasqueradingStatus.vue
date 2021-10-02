<template>
  <div
    v-if="masquerading"
    id="masquerading-status"
    class="clickable has-tooltip-right"
    data-tooltip="You are masquerading as audience. Click to go back to the player mode!"
    @click="exitAudienceView"
  >
    <Icon src="incognito.svg" :size="36" />
  </div>
</template>

<script>
import { computed } from "@vue/reactivity";
import { useStore } from "vuex";
import Icon from "@/components/Icon.vue";

export default {
  components: { Icon },
  setup: () => {
    const store = useStore();
    const masquerading = computed(() => store.state.stage.masquerading);
    const exitAudienceView = () => {
      store.commit('stage/TOGGLE_MASQUERADING');
    }

    return { masquerading, exitAudienceView };
  },
};
</script>

<style scoped lang="scss">
#masquerading-status {
  position: absolute;
  z-index: 10;
  top: 8px;
  left: 8px;
}
</style>