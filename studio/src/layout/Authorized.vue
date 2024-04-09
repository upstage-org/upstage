<template>
    <a-layout>
        <Sidebar />
        <a-layout class="h-screen space-y-2 p-2" :style="{ background: route?.meta?.background }">
            <router-view />
        </a-layout>
    </a-layout>
</template>

<script>
import Sidebar from "components/Sidebar.vue";
import Footer from "components/Footer.vue";
import OneTimePurchase from "components/payment/OneTimePurchase.vue";
import PurchasePopup from "components/payment/PurchasePopup.vue";
import { useStore } from "vuex";
import { ref, watchEffect } from "vue";
import { useRoute } from "vue-router";

export default {
    components: { Footer, OneTimePurchase, PurchasePopup },
    setup: () => {
        const store = useStore();
        const enableDonate = ref(false);
        const route = useRoute();
        watchEffect(() => {
            enableDonate.value = store.getters["config/enableDonate"];
        });

        return { enableDonate, route };
    },
};
</script>