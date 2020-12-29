<template>
  <a v-if="link" class="navbar-item" :href="link" target="_blank">
    <img src="@/assets/upstage.png" width="80" />
  </a>
  <router-link v-else class="navbar-item" to="/">
    <img src="@/assets/upstage.png" width="80" />
  </router-link>
</template>

<script>
export default {
  props: ["link"],
};
</script>