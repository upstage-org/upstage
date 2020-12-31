<template>
  <span
    id="connection-status"
    class="tag is-dark is-medium"
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
    <span>{{ status }}</span>
  </span>
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

<style scoped>
#connection-status {
  position: fixed;
  right: 120px;
  top: 5px;
}
</style>