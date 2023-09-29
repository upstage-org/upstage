<template>
  <section class="hero is-small is-warning is-bold">
    <div class="hero-body">
      <Breadcrumb description="Manage players and system settings" />
      <h1 class="title is-inline">{{ $route.name }}</h1>
    </div>
  </section>
  <section class="section">
    <div class="columns" :class="{ 'is-loading': !user }">
      <div class="column is-narrow" v-if="notInIframe">
        <aside class="menu box has-background-light">
          <p class="menu-label">{{ $t("users") }}</p>
          <ul class="menu-list">
            <li>
              <router-link
                to="/backstage/admin/player-management"
                exact-active-class="is-active"
                >{{ $t("player_management") }}</router-link
              >
            </li>
            <li>
              <router-link
                to="/backstage/admin/batch-user-creation"
                exact-active-class="is-active"
                >{{ $t("batch_user_creation") }}</router-link
              >
            </li>
          </ul>
          <p class="menu-label">{{ $t("system") }}</p>
          <ul class="menu-list">
            <li>
              <router-link
                to="/backstage/admin/foyer-customisation"
                exact-active-class="is-active"
                >{{ $t("foyer_customisation") }}</router-link
              >
            </li>
            <li>
              <router-link
                to="/backstage/admin/email-notification"
                exact-active-class="is-active"
                >{{ $t("email_notification") }}</router-link
              >
            </li>
            <li>
              <router-link
                to="/backstage/admin/system-configuration"
                exact-active-class="is-active"
                >{{ $t("system_configuration") }}</router-link
              >
            </li>
          </ul>
        </aside>
      </div>
      <div class="column is-expanded lite-scroller">
        <router-view v-if="user" />
      </div>
    </div>
  </section>
</template>

<script>
import { displayName } from "@/utils/auth";
import { useStore } from "vuex";
import { computed } from "vue";
import Breadcrumb from "@/components/Breadcrumb";
export default {
  components: { Breadcrumb },
  setup: () => {
    const store = useStore();
    const user = computed(() => store.state.user.user);
    const notInIframe = computed(() => window.self === window.top);
    return { displayName, user, notInIframe };
  },
};
</script>

<style lang="scss" scoped>
@media screen and (min-width: 769px) and (max-width: 1280px) {
  .lite-scroller {
    width: 0;
    .table-wrapper {
      padding-bottom: 0;
    }
  }
}
</style>
