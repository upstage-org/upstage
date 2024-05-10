<template>
    <NavBar />
    <div id="main-layout">
      <router-view />
      <OneTimePurchase v-if="enableDonate" />
      <PurchasePopup v-if="enableDonate" />
    </div>
    <Footer />
  </template>
  
  <script>
  import Footer from "components/Footer.vue";
  import NavBar from "components/NavBarHome.vue";
  import OneTimePurchase from "components/payment/OneTimePurchase.vue";
  import PurchasePopup from "components/payment/PurchasePopup.vue";
  import { useStore } from "vuex";
  import { ref, watchEffect } from "vue";
  export default {
    components: { NavBar, Footer, OneTimePurchase, PurchasePopup },
    setup: () => {
      const store = useStore();
      const enableDonate = ref(false);
      watchEffect(() => {
        enableDonate.value = store.getters["config/enableDonate"];
      });
  
      return { enableDonate };
    },
  };
  </script>
  
  <style>
  #main-layout {
    min-height: calc(100vh - 120px);
  }
  </style>
  