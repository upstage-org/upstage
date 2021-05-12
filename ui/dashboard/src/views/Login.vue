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
export default {
  components: { LoginForm },
  methods: {
    onLoginSuccess() {
      this.$router.push({ name: "Backstage" });
    },
  },
};
</script>

<style>
</style>
