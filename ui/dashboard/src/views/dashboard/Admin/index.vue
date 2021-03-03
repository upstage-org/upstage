<template>
  <section class="hero is-small is-warning is-bold">
    <div class="hero-body">
      <h1 class="title">UpStage Admin</h1>
    </div>
  </section>
  <div class="columns" :class="{ 'is-loading': !user }">
    <div class="column is-4">
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
        </ul>
      </aside>
    </div>
    <div class="column is-8">
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