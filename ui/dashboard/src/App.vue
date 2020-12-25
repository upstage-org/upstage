<template>
  <NavBar />
  <div id="main-content">
    <router-view />
  </div>
  <Footer />
</template>

<script>
import NavBar from "@/components/NavBar";
import Footer from "@/components/Footer";
export default {
  components: { NavBar, Footer },
};
</script>

<style lang="scss">
#main-content {
  min-height: calc(100vh - 120px);
  padding: 10px;
}
</style>
