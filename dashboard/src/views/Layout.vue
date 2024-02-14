<template>
  <NavBar />
  <div id="main-content">
    <router-view />
    <OneTimePurchase v-if="enableDonate" />
    <PurchasePopup v-if="enableDonate" />
  </div>
  <Footer />
</template>

<script>
import Footer from "@/components/Footer";
import NavBar from "@/components/NavBar";
import OneTimePurchase from "@/components/payment/OneTimePurchase";
import PurchasePopup from "@/components/payment/PurchasePopup";
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
#main-content {
  min-height: calc(100vh - 120px);
}
</style>
