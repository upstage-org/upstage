<template>
  <section class="hero is-small is-light is-bold">
    <div class="hero-body">
      <Breadcrumb :description="user ? displayName(user) + '\'s profile' : ''" />
      <h1 class="title is-inline">{{ $route.name }}</h1>
    </div>
  </section>
  <div class="columns" :class="{ 'is-loading': !user }">
    <div class="column is-narrow">
      <aside class="menu box has-background-light mx-4">
        <ul class="menu-list">
          <li>
            <router-link
              to="/backstage/profile/information"
              exact-active-class="is-active"
            >
              Update Information
            </router-link>
          </li>
          <li>
            <router-link
              to="/backstage/profile/change-password"
              exact-active-class="is-active"
            >
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