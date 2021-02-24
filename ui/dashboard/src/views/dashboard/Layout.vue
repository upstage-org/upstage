<template>
  <nav class="navbar" role="navigation" aria-label="main navigation">
    <div class="navbar-menu is-active">
      <div class="navbar-start">
        &nbsp;
        <router-link class="navbar-item" to="/dashboard">
          Dashboard
        </router-link>
        <div class="vertical-divider" />
        <router-link class="navbar-item" to="/dashboard/media">
          Media
        </router-link>
        <div class="vertical-divider" />
        <router-link class="navbar-item" to="/dashboard/my-stages">
          My Stages
        </router-link>
        <div class="vertical-divider" />
        <router-link class="navbar-item" to="/dashboard/profile">
          Profile
        </router-link>
      </div>
    </div>

    <div class="navbar-brand">
      <Logo />
    </div>
  </nav>
  <div id="main-content">
    <router-view />
  </div>
  <Footer />
</template>

<script>
import Footer from "@/components/Footer";
import Logo from "@/components/Logo";
export default {
  components: { Footer, Logo },
};
</script>

<style>
#main-content {
  min-height: calc(100vh - 120px);
}
</style>