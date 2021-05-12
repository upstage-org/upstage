<template>
  <nav class="breadcrumb mb-4" aria-label="breadcrumbs">
    <ul>
      <li v-for="route in $route.matched" :key="route">
        <router-link :to="route.path" aria-current="page">
          {{ route.name }}
        </router-link>
      </li>
      <span>👉 {{ description }}</span>
    </ul>
  </nav>
</template>

<script>
export default {
  props: {
    description: String,
  },
};
</script>

<style>
</style>