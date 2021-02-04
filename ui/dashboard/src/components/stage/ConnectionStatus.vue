<template>
  <div id="connection-status">
    <span
      class="tag is-light is-small"
      :class="{
        'is-danger': status === 'LIVE',
        'is-warning': status === 'CONNECTING',
      }"
    >
      <span class="icon" v-show="status !== 'OFFLINE'">
        <i ref="dot" class="fas fa-circle"></i>
      </span>
      <span class="icon" v-show="status === 'OFFLINE'">
        <i class="far fa-circle"></i>
      </span>
      <span class="status-text">{{ status }}</span>
    </span>
  </div>
</template>

<script>
import { useStore } from "vuex";
import anime from "animejs";
import { ref, computed, onMounted } from "vue";
export default {
  setup: () => {
    const store = useStore();
    const dot = ref();
    const status = computed(() => store.state.stage.status);

    onMounted(() => {
      anime({
        targets: dot.value,
        opacity: [1, 0, 1],
        duration: 2000,
        loop: true,
      });
    });

    return {
      status,
      dot,
    };
  },
};
</script>

<style scoped lang="scss">
#connection-status {
  position: fixed;
  right: 12px;
  top: 50px;
  width: 150px;
  text-align: center;

  @media screen and (max-width: 767px) {
    right: unset;
    top: 8px;
    left: 0;
  }
}
</style>