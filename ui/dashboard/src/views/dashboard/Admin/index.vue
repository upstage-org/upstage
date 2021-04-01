<template>
  <section class="hero is-small is-warning is-bold">
    <div class="hero-body">
      <h1 class="title">UpStage Admin</h1>
    </div>
  </section>
  <div class="columns" :class="{ 'is-loading': !user }">
    <div class="column is-narrow">
      <aside class="menu box has-background-light mx-4">
        <ul class="menu-list">
          <li>
            <router-link
              to="/dashboard/admin/approval"
              exact-active-class="is-active"
            >
              Registration Approval
            </router-link>
          </li>
          <li>
            <router-link
              to="/dashboard/admin/reset-password"
              exact-active-class="is-active"
            >
              Reset Password
            </router-link>
          </li>
          <li>
            <router-link
              to="/dashboard/admin/switch-role"
              exact-active-class="is-active"
            >
              Switch Role
            </router-link>
          </li>
          <li>
            <router-link
              to="/dashboard/admin/delete-user"
              exact-active-class="is-active"
            >
              Delete User
            </router-link>
          </li>
          <li>
            <router-link
              to="/dashboard/admin/profile-management"
              exact-active-class="is-active"
            >
              Profile Management
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
export default {
  setup: () => {
    const store = useStore();
    const user = computed(() => store.state.user.user);
    return { displayName, user };
  },
};
</script>

<style>
</style>