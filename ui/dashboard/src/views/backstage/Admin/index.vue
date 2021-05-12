<template>
  <section class="hero is-small is-warning is-bold">
    <div class="hero-body">
      <Breadcrum description="Manage players and system settings" />
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
              to="/backstage/admin/approval"
              exact-active-class="is-active"
            >
              Registration Approval
            </router-link>
          </li>
          <li>
            <router-link
              to="/backstage/admin/reset-password"
              exact-active-class="is-active"
            >
              Reset Password
            </router-link>
          </li>
          <li>
            <router-link
              to="/backstage/admin/switch-role"
              exact-active-class="is-active"
            >
              Switch Role
            </router-link>
          </li>
          <li>
            <router-link
              to="/backstage/admin/delete-user"
              exact-active-class="is-active"
            >
              Delete User
            </router-link>
          </li>
          <li>
            <router-link
              to="/backstage/admin/profile-management"
              exact-active-class="is-active"
            >
              Profile Management
            </router-link>
          </li>
          <li>
            <router-link
              to="/backstage/admin/upload-limit"
              exact-active-class="is-active"
            >
              Upload Limit
            </router-link>
          </li>
        </ul>
        <p class="menu-label">System</p>
        <ul class="menu-list">
          <li>
            <router-link
              to="/backstage/admin/system-configurations"
              exact-active-class="is-active"
            >
              System Configurations
            </router-link>
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
import Breadcrum from "@/components/Breadcrum";
export default {
  components: { Breadcrum },
  setup: () => {
    const store = useStore();
    const user = computed(() => store.state.user.user);
    return { displayName, user };
  },
};
</script>

<style>
</style>