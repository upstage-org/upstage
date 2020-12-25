<template>
  <nav class="navbar" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <router-link class="navbar-item" to="/">
        <img src="@/assets/upstage.png" width="80" />
      </router-link>

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

    <div :class="{ 'navbar-menu': true, 'is-active': expanded }">
      <div class="navbar-start">
        <router-link class="navbar-item" to="/">Home</router-link>
        <router-link class="navbar-item" to="/stage">Stages</router-link>
        <router-link class="navbar-item" to="/dashboard">Dashboard</router-link>

        <div class="navbar-item has-dropdown is-hoverable">
          <a class="navbar-link"> More </a>
          <div class="navbar-dropdown">
            <a
              class="navbar-item"
              href="https://github.com/upstage-org/mobilise/"
              target="_blank"
            >
              GitHub
            </a>
            <a
              class="navbar-item"
              href="https://github.com/upstage-org/documentation"
              target="_blank"
            >
              Documentation
            </a>
          </div>
        </div>
      </div>

      <div class="navbar-end">
        <div class="navbar-item">
          <div class="buttons">
            <router-link to="/login" class="button is-primary">
              <strong>Login</strong>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { ref } from "vue";
export default {
  setup() {
    const expanded = ref(false);
    const toggleExpanded = () => (expanded.value = !expanded.value);
    return { expanded, toggleExpanded };
  },
};
</script>

<style lang="scss">
nav {
  a {
    color: #2c3e50;

    &.router-link-exact-active {
      font-weight: bold;
      color: #42b983;
    }
  }
  @media screen and (max-width: 1023px) {
    .navbar-menu {
      position: absolute;
      width: 100%;
    }
    .navbar-end a {
      margin-left: auto;
    }
  }
}
</style>