<template>
  <div class="columns is-mobile is-centered is-vcentered foyer-background">
    <div
      class="column is-three-quarters-mobile is-two-thirds-tablet is-half-desktop is-one-third-widescreen"
    >
      <LoginForm @success="onLoginSuccess" />
    </div>
  </div>
</template>

<script>
import LoginForm from "@/components/LoginForm";
import configs from "@/config";
export default {
  components: { LoginForm },
  methods: {
    onLoginSuccess() {
      window.location.href = configs.STUDIO_ENDPOINT;
    },
  },
};
</script>

<style></style>
