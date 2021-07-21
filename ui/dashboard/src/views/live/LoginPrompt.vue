<template>
  <div class="modal" :class="{ 'is-active': showing }">
    <div class="modal-background" @click="enterAsAudience"></div>
    <div ref="modal" class="modal-content">
      <LoginForm v-if="showLoginForm" @success="onLoginSuccess" />
      <div v-else class="card">
        <header class="card-header">
          <p class="card-header-title">Click anywhere to enter the stage</p>
        </header>
        <div class="card-content">
          <div class="content">
            <label class="label" style="font-weight: normal">
              Choose a nickname if you want one:
            </label>
            <InputButtonPostfix
              v-model="nickname"
              placeholder="Guest"
              icon="fas fa-sign-in-alt"
              title="Choose a nickname"
              @ok="enterAsAudience"
            />
          </div>
        </div>
      </div>
    </div>
    <button
      v-if="showLoginForm"
      class="button is-light is-outlined mt-4"
      @click="showLoginForm = false"
    >
      <span class="icon">
        <i class="fas fa-chevron-left"></i>
      </span>
      <span>Enter as Audience</span>
    </button>
    <button
      v-else
      class="button is-light is-outlined mt-4"
      @click="showLoginForm = true"
    >
      <span>Player Login</span>
      <span class="icon">
        <i class="fas fa-chevron-right"></i>
      </span>
    </button>
  </div>
</template>

<script>
import LoginForm from "@/components/LoginForm.vue";
import InputButtonPostfix from "@/components/form/InputButtonPostfix";
import { computed, onMounted, ref, watch } from "vue";
import { useStore } from "vuex";
import anime from "animejs";
import { notification } from "@/utils/notification";

export default {
  components: { LoginForm, InputButtonPostfix },
  setup: () => {
    const store = useStore();
    const loggedIn = computed(() => store.getters["auth/loggedIn"]);
    const showing = ref(!loggedIn.value);
    const showLoginForm = ref(false);
    const nickname = ref();
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
        store.dispatch("stage/joinStage");
        close();
      }
    });

    const close = () => (showing.value = false);

    const enterAsAudience = () => {
      if (!showLoginForm.value) {
        store
          .dispatch("user/saveNickname", { nickname: nickname.value })
          .then((nickname = "Guest") => {
            notification.success(
              "Welcome to the stage! Your nickname is " + nickname + "!"
            );
            close();
          });
      }
    };

    const onLoginSuccess = () => {
      store.dispatch("stage/reloadPermission");
    };

    return {
      showing,
      close,
      modal,
      showLoginForm,
      nickname,
      enterAsAudience,
      onLoginSuccess,
    };
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