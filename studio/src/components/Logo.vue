<template>
  <a v-if="link" class="navbar-item" :href="link" :target="target || '_self'">
    <img src="assets/upstage.png" />
  </a>
  <router-link v-else class="navbar-item" :to="to ?? '/'">
    <img src="assets/upstage.png" />
  </router-link>
</template>

<script>
export default {
  props: ["link", "to", "target"],
};
</script>
