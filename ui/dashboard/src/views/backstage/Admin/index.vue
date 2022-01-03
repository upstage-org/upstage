<template>
  <section class="hero is-small is-warning is-bold">
    <div class="hero-body">
      <Breadcrumb description="Manage players and system settings" />
      <h1 class="title is-inline">{{ $route.name }}</h1>
    </div>
  </section>
  <div class="columns" :class="{ 'is-loading': !user }">
    <div class="column is-narrow">
      <aside class="menu box has-background-light mx-4">
        <p class="menu-label">Users</p>
        <ul class="menu-list">
          <li>
            <router-link
              to="/backstage/admin/player-management"
              exact-active-class="is-active"
            >Player Management</router-link>
          </li>
          <li>
            <router-link
              to="/backstage/admin/batch-user-creation"
              exact-active-class="is-active"
            >Batch User Creation</router-link>
          </li>
        </ul>
        <p class="menu-label">System</p>
        <ul class="menu-list">
          <li>
            <router-link
              to="/backstage/admin/system-configurations"
              exact-active-class="is-active"
            >System Configurations</router-link>
          </li>
          <li>
            <router-link
              to="/backstage/admin/foyer-customisation"
              exact-active-class="is-active"
            >Foyer Customisation</router-link>
          </li>
          <li>
            <router-link
              to="/backstage/admin/email-notification"
              exact-active-class="is-active"
            >Email Notification</router-link>
          </li>
        </ul>
      </aside>
    </div>
    <div class="column">
      <div class="pt-4 pr-4 pb-4">
        <router-view v-if="user" />
      </div>
    </div>
  </div>
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
    return { displayName, user };
  },
};
</script>

<style>
</style>