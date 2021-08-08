<template>
  <div class="event-indicator">
    <div
      v-for="event in events"
      :key="event.id"
      :style="{ left: position(event) + '%' }"
    ></div>
  </div>
</template>

<script>
import { computed } from "@vue/runtime-core";
import { useStore } from "vuex";
export default {
  setup() {
    const store = useStore();
    const events = computed(() => store.state.stage.model.events);
    const begin = computed(() =>
      Number(store.state.stage.replay.timestamp.begin)
    );
    const end = computed(() => Number(store.state.stage.replay.timestamp.end));
    const duration = computed(() => end.value - begin.value);

    const position = (event) => {
      return (
        ((Number(event.mqttTimestamp) - begin.value) * 100) / duration.value
      );
    };

    return {
      events,
      position,
    };
  },
};
</script>

<style scoped lang="scss">
@import "@/styles/bulma";
.event-indicator {
  pointer-events: none;
  position: relative;
  width: 100%;
  height: 8px;
  top: -24px;
  > div {
    position: absolute;
    height: 100%;
    width: 1px;
    background-color: $primary;
  }
}
</style>