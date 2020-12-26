<template>
  <router-view />
</template>

<script>
</script>

<style lang="scss">
html {
  overflow-y: auto !important;
}
nav {
  a {
    color: #2c3e50;

    &.router-link-exact-active {
      font-weight: bold;
      color: #42b983;
    }
  }
}
</style>
