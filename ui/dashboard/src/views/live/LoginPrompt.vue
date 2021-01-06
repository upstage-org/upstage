<template>
  <div class="modal" :class="{ 'is-active': showing }">
    <div class="modal-background"></div>
    <div ref="modal" class="modal-content">
      <LoginForm />
    </div>
    <button class="button is-primary mt-4" @click="close">
      <span class="icon">
        <i class="fas fa-sign-in-alt"></i>
      </span>
      <span>Login as Guest</span>
    </button>
  </div>
</template>

<script>
import LoginForm from "@/components/LoginForm.vue";
import { computed, onMounted, ref, watch } from "vue";
import { useStore } from "vuex";
import anime from "animejs";

export default {
  components: { LoginForm },
  setup: () => {
    const store = useStore();
    const loggedIn = computed(() => store.getters["auth/loggedIn"]);
    const showing = ref(!loggedIn.value);
    const modal = ref();

    onMounted(() => {
      anime({
        targets: modal.value,
        rotate: ["-3deg", "3deg", "0deg"],
        duration: 100,
        direction: "alternate",
        loop: 5,
        easing: "easeOutBack",
      });
    });

    watch(loggedIn, () => {
      if (loggedIn.value) {
        close();
      }
    });

    const close = () => (showing.value = false);
    return { showing, close, modal };
  },
};
</script>
<style scoped lang="scss">
.modal-close {
  position: relative;
}
.modal-content {
  max-width: 500px;
}
</style>