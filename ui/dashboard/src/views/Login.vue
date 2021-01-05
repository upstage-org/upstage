<template>
  <div class="login-page columns is-mobile is-centered is-vcentered">
    <div
      class="column is-three-quarters-mobile is-two-thirds-tablet is-half-desktop is-one-third-widescreen is-one-quarter-fullhd"
    >
      <LoginForm />
    </div>
  </div>
</template>

<script>
import LoginForm from "@/components/LoginForm";
export default {
  components: { LoginForm },
};
</script>

<style>
.login-page {
  height: 80vh;
}
</style>
