<template>
  <nav class="navbar" role="navigation" aria-label="main navigation">
    <div :class="{ 'navbar-menu': true, 'is-active': expanded }">
      <div class="navbar-start">
        &nbsp;
        <router-link class="navbar-item" to="/backstage/stages">
          <span>
            <i class="fas fa-person-booth"></i>
            Stages
          </span>
        </router-link>
        <div class="vertical-divider" />
        <a class="navbar-item" :href="configs.STUDIO_ENDPOINT" target="_blank">
          <span>
            <i class="fas fa-magic has-text-info"></i>
            Studio
          </span>
        </a>
        <div class="vertical-divider" />
        <router-link class="navbar-item" to="/backstage/profile/">
          <span>
            <i class="fas fa-user"></i>
            Profile
          </span>
        </router-link>
        <template v-if="isAdmin">
          <div class="vertical-divider" />
          <router-link class="navbar-item" to="/backstage/admin/">
            <span>
              <i class="fas fa-shield-alt has-text-warning"></i>
              Admin
            </span>
          </router-link>
        </template>
      </div>
    </div>

    <div class="navbar-brand">
      <Logo />
      <a
        role="button"
        class="navbar-burger"
        aria-label="menu"
        aria-expanded="false"
        @click="toggleExpanded"
      >
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
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
import { useStore } from "vuex";
import { computed, ref } from "vue";
import configs from "@/config";

export default {
  components: { Footer, Logo },
  setup: () => {
    const store = useStore();

    const isAdmin = computed(() => store.getters["user/isAdmin"]);
    const expanded = ref(false);
    const toggleExpanded = () => (expanded.value = !expanded.value);

    return { isAdmin, expanded, toggleExpanded, configs };
  },
};
</script>

<style scoped>
#main-content {
  min-height: calc(100vh - 120px);
}
@media screen and (max-width: 1023px) {
  .navbar-brand {
    position: absolute;
    top: 0;
    width: 100%;
  }
  .navbar-menu .navbar-item:first-child {
    margin-left: 8px;
    margin-top: 24px;
  }
}
</style>