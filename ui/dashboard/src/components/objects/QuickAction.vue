<template>
  <div
    class="quick-action"
    v-show="showQuickActions"
    @mousedown.stop="keepActive"
    @mouseup.stop="keepActive"
  >
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
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
export default {
  props: ["object", "active"],
  emits: ["update:active"],
  setup: (props, { emit }) => {
    const store = useStore();
    const isHolding = computed(
      () => props.object.id === store.state.user.avatarId
    );

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

    const holdable = computed(() =>
      ["avatar", "drawing"].includes(props.object.type)
    );
    const activeMovable = computed(() => store.state.stage.activeMovable);
    const showQuickActions = computed(
      () =>
        isHolding.value ||
        (!holdable.value && activeMovable.value === props.object.id)
    );

    return {
      deleteObject,
      keepActive,
      toggleLiveAction,
      isHolding,
      showQuickActions,
    };
  },
};
</script>

<style scoped lang="scss">
.quick-action {
  position: absolute;
  width: min-content;
  right: -40px;
  button {
    width: 16px;
    margin-bottom: 4px;
  }
}
</style>