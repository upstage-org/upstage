<template>
  <Logo id="live-logo" />
  <div id="main-content">
    <router-view />
  </div>
</template>

<script>
import Logo from "@/components/Logo";
export default {
  components: { Logo },
};
</script>

<style>
#main-content {
  min-height: calc(100vh - 120px);
}
#live-logo {
  position: fixed;
  right: 10px;
}
</style>