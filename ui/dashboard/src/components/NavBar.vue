<template>
  <nav class="navbar" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <Logo link="https://www.upstage.org.nz" />
      <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" @click="toggleExpanded">
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>
    <LanguageSelector />

    <div :class="{ 'navbar-menu': true, 'is-active': expanded }">
      <div class="navbar-start">
        <div v-if="!navigations" class="navbar-item" style="text-transform: none;">Cannot display navigation properly,
          please check your menu syntax in Admin section!</div>
        <template v-else>
          <template v-for="(menu, i) in navigations" :key="i">
            <div v-if="menu.children" class="navbar-item has-dropdown is-hoverable">
              <a v-if="menu.url" class="navbar-link is-arrowless" :href="menu.url"
                :target="menu.url?.startsWith('http') ? '_blank' : ''">{{ menu.title }}</a>
              <a v-else class="navbar-link is-arrowless">{{ menu.title }}</a>
              <div class="navbar-dropdown">
                <a v-for="(submenu, j) in menu.children" :key="{ j }" class="navbar-item" :href="submenu.url"
                  :target="submenu.url?.startsWith('http') ? '_blank' : ''">{{ submenu.title }}</a>
              </div>
            </div>
            <a v-else class="navbar-item" :href="menu.url" :target="menu.url?.startsWith('http') ? '_blank' : ''">{{
                menu.title
            }}</a>
            <div v-if="i < navigations.length - 1" class="vertical-divider" />
          </template>
        </template>
      </div>

      <div class="navbar-end">
        <template v-if="loggedIn">
          <router-link to="/backstage" class="button is-primary m-2">
            <strong>{{ $t("backstage") }}</strong>
          </router-link>
          <button @click="logout" class="button m-2 mr-6">
            <strong>{{ $t("logout") }}</strong>
          </button>
        </template>
        <template v-else>
          <router-link to="/login" class="button is-primary m-2">
            <strong>{{ $t("login") }}</strong>
          </router-link>
          <router-link v-if="foyer.showRegistration" to="/register" class="button is-primary m-2 mr-6">
            <strong>{{ $t("register") }}</strong>
          </router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script>
import { computed, ref } from "vue";
import { loggedIn, logout } from "@/utils/auth";
import { useStore } from "vuex";
import Logo from "./Logo";
import LanguageSelector from "./LanguageSelector.vue";

export default {
  components: { Logo, LanguageSelector },
  setup() {
    const store = useStore();
    const expanded = ref(false);
    const toggleExpanded = () => (expanded.value = !expanded.value);

    const navigations = computed(() => store.getters["config/navigations"]);
    const foyer = computed(() => store.getters["config/foyer"]);

    return {
      expanded,
      toggleExpanded,
      loggedIn,
      logout,
      navigations,
      foyer
    };
  },
};
</script>

<style lang="scss">
@media screen and (max-width: 1023px) {
  .navbar-menu {
    position: absolute;
    width: 100%;
  }

  .navbar-end a {
    margin-left: auto;
  }
}
</style>