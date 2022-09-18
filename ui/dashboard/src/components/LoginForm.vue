<template>
  <form v-if="!resetMode" @submit.prevent="submit">
    <div class="card">
      <header class="card-header">
        <p class="card-header-title">{{ $t("enter_username_and_password_to_login") }}</p>
      </header>
      <div class="card-content">
        <div class="content">
          <div class="field">
            <p class="control has-icons-left">
              <input class="input" v-model="username" placeholder="Username" required />
              <span class="icon is-small is-left">
                <i class="fas fa-user"></i>
              </span>
            </p>
          </div>
          <div class="field">
            <p class="control has-icons-left has-icons-right">
              <input class="input" :type="showPassword ? 'text' : 'password'" placeholder="Password" v-model="password"
                required />
              <span class="icon is-small is-left">
                <i class="fas fa-lock"></i>
              </span>
              <a class="icon is-small is-right" style="pointer-events: all" @click="toggleShowPassword">
                <i :class="`fas fa-${showPassword ? 'eye-slash' : 'eye'}`"></i>
              </a>
              <a class="help has-text-right" @click="resetMode = true">Forgot password?</a>
            </p>
            <p>
              {{ $t("tos.login") }}
              <TermsOfService />
            </p>
          </div>
        </div>
      </div>
      <footer class="card-footer">
        <button type="submit" class="card-footer-item is-white button has-text-primary"
          :class="{ 'is-loading': loading }">
          <span>{{ $t("login") }}</span>
          <span class="icon is-medium">
            <i class="fas fa-chevron-right"></i>
          </span>
        </button>
      </footer>
    </div>
  </form>
  <form v-else @submit.prevent="resetPassword">
    <div class="card">
      <header class="card-header">
        <p class="card-header-title">{{ $t("reset_your_password") }}</p>
      </header>
      <div v-if="resetStep === 1" class="card-content">
        <div class="content">
          <p>Please provide us your username or email so that we can send you a verify code:</p>
          <div class="field">
            <p class="control has-icons-left">
              <input class="input" v-model="username" placeholder="Username or email" required />
              <span class="icon is-small is-left">
                <i class="fas fa-user"></i>
              </span>
            </p>
          </div>
        </div>
      </div>
      <div v-if="resetStep === 2" class="card-content">
        <div class="content">
          <p>Please enter the OTP code that we've sent to your email:</p>
          <div class="field">
            <p class="control has-icons-left">
              <input class="input" v-model="otp" placeholder="XXXXXX" required maxlength="6" />
              <span class="icon is-small is-left">
                <i class="fas fa-key"></i>
              </span>
            </p>
          </div>
        </div>
      </div>
      <div v-if="resetStep === 3" class="card-content">
        <div class="content">
          <p>Please enter your new password:</p>
          <div class="field">
            <p class="control has-icons-left has-icons-right">
              <input class="input" :type="showPassword ? 'text' : 'password'" placeholder="Password" v-model="password"
                required />
              <span class="icon is-small is-left">
                <i class="fas fa-lock"></i>
              </span>
              <a class="icon is-small is-right" style="pointer-events: all" @click="toggleShowPassword">
                <i :class="`fas fa-${showPassword ? 'eye-slash' : 'eye'}`"></i>
              </a>
            </p>
          </div>
          <div class="field">
            <p class="control has-icons-left has-icons-right">
              <input class="input" :type="showPassword ? 'text' : 'password'" placeholder="Confirm Password"
                v-model="passwordConfirm" required />
              <span class="icon is-small is-left">
                <i class="fas fa-lock"></i>
              </span>
              <a class="icon is-small is-right" style="pointer-events: all" @click="toggleShowPassword">
                <i :class="`fas fa-${showPassword ? 'eye-slash' : 'eye'}`"></i>
              </a>
              <span class="help is-danger" v-if="password && passwordConfirm && (password !== passwordConfirm)">Confirm
                password mismatch!</span>
            </p>
          </div>
        </div>
      </div>
      <footer class="card-footer">
        <button v-if="resetStep < 3" type="submit" class="card-footer-item is-white button has-text-primary"
          :class="{ 'is-loading': loading }">
          <span>{{ $t("next") }}</span>
          <span class="icon is-medium">
            <i class="fas fa-chevron-right"></i>
          </span>
        </button>
        <button v-else type="submit" class="card-footer-item is-white button has-text-primary"
          :class="{ 'is-loading': loading }"
          :disabled="!password || !passwordConfirm || (password !== passwordConfirm)">
          <span>{{ $t("finish") }}</span>
          <span class="icon is-medium">
            <i class="fas fa-chevron-right"></i>
          </span>
        </button>
      </footer>
    </div>
  </form>
</template>

<script setup>
import TermsOfService from "@/components/TermsOfService.vue";
import { userGraph } from "@/services/graphql";
import { useMutation } from "@/services/graphql/composable";
import { notification } from "@/utils/notification";
import { ref, defineEmits } from "vue";
import { useStore } from "vuex";

const emit = defineEmits(['success']);
const showPassword = ref(false)
const username = ref('')
const password = ref('')
const loading = ref(false)
const store = useStore()
const resetMode = ref(false)

const toggleShowPassword = () => {
  showPassword.value = !showPassword.value;
}
const submit = () => {
  const user = {
    username: username.value.trim(),
    password: password.value,
  };
  loading.value = true;
  store
    .dispatch("auth/login", user)
    .then(() => {
      emit("success");
    })
    .finally(() => {
      loading.value = false;
    });
}

const { save: step1 } = useMutation(userGraph.requestPasswordReset);
const resetStep = ref(1);
const requestPasswordReset = async () => {
  loading.value = true;
  await step1(res => {
    notification.success(res.requestPasswordReset.message)
    username.value = res.requestPasswordReset.username
    resetStep.value = 2
  }, {
    usernameOrEmail: username.value.trim()
  });
  loading.value = false;
}

const otp = ref('')
const { save: step2 } = useMutation(userGraph.verifyPasswordReset);
const verifyOTP = async () => {
  loading.value = true;
  await step2(res => {
    notification.success(res.verifyPasswordReset.message)
    resetStep.value = 3
  }, {
    otp: otp.value.trim(),
    username: username.value.trim()
  });
  loading.value = false;
}

const { save: step3 } = useMutation(userGraph.passwordReset);
const passwordConfirm = ref('')
const processPasswordReset = async () => {
  loading.value = true;
  await step3(res => {
    notification.success(res.passwordReset.message)
    resetStep.value = 1
    resetMode.value = false
  }, {
    otp: otp.value.trim(),
    username: username.value.trim(),
    password: password.value
  });
  loading.value = false;
}

const resetPassword = () => {
  if (resetStep.value === 1) {
    requestPasswordReset()
  }
  if (resetStep.value === 2) {
    verifyOTP()
  }
  if (resetStep.value === 3) {
    processPasswordReset()
  }
}
</script>

<style>
</style>
