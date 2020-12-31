<template>
  <span
    id="connection-status"
    class="tag is-dark is-medium"
    :class="{
      'is-danger': status === 'LIVE',
      'is-warning': status === 'CONNECTING',
    }"
  >
    <span class="icon">
      <i ref="dot" class="fas fa-circle"></i>
    </span>
    <span>{{ status }}</span>
  </span>
</template>

<script>
import { useStore } from "vuex";
import anime from "animejs";
import { ref, computed, watchEffect, onMounted } from "vue";
export default {
  setup: () => {
    const store = useStore();
    const dot = ref();
    const status = computed(() => store.state.stage.status);
    const animation = ref();

    onMounted(() => {
      animation.value = anime({
        targets: dot.value,
        opacity: [1, 0, 1],
        duration: 2000,
        loop: true,
        autoplay: false,
      });
    });

    watchEffect(() => {
      if (status.value === "OFFLINE") {
        animation.value?.pause();
      } else {
        animation.value?.play();
      }
    });

    return {
      status,
      dot,
    };
  },
};
</script>

<style scoped>
#connection-status {
  position: fixed;
  right: 120px;
  top: 5px;
}
</style>