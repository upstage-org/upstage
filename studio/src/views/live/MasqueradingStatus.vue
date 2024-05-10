<template>
  <a-tooltip title="You are masquerading as audience. Click to go back to the player mode!">
    <div v-if="masquerading" id="masquerading-status" class="clickable has-tooltip-left" @click="exitAudienceView">
      <Icon src="incognito.svg" :size="36" />
    </div>
  </a-tooltip>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import Icon from "components/Icon.vue";

export default {
  components: { Icon },
  setup: () => {
    const store = useStore();
    const masquerading = computed(() => store.state.stage.masquerading);
    const exitAudienceView = () => {
      store.commit("stage/TOGGLE_MASQUERADING");
    };

    return { masquerading, exitAudienceView };
  },
};
</script>

<style scoped lang="scss">
#masquerading-status {
  position: absolute;
  z-index: 10;
  top: 76px;
  right: 16px;
}
</style>
