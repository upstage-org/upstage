<template>
  <section class="hero is-small is-dark is-bold">
    <div class="hero-body">
      <h1 class="title">Player Profile</h1>
      <h2 class="subtitle" v-if="user">
        <ul>
          <li>{{ displayName(user) }}'s profile</li>
        </ul>
      </h2>
    </div>
  </section>
  <div class="columns" :class="{ 'is-loading': !user }">
    <div class="column is-narrow">
      <aside class="menu box has-background-light mx-4">
        <ul class="menu-list">
          <li>
            <router-link
              to="/dashboard/profile/"
              exact-active-class="is-active"
            >
              Update Information
            </router-link>
          </li>
          <li>
            <router-link to="change-password" exact-active-class="is-active">
              Change Password
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