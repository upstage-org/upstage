<template>
  <NavBar />
  <div id="main-content">
    <router-view />
    <OneTimePurchase />
    <PurchasePopup />
  </div>
  <Footer/>
</template>

<script>
import NavBar from "@/components/NavBar";
import Footer from "@/components/Footer";
import OneTimePurchase from "@/components/stage/Payment/OneTimePurchase";
import PurchasePopup from "@/components/stage/Payment/PurchasePopup";
export default {
  components: { NavBar, Footer, OneTimePurchase, PurchasePopup },
};
</script>

<style>
#main-content {
  min-height: calc(100vh - 120px);
}
</style>