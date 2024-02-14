<template>
  <div id="main-content">
    <router-view />
  </div>
  <Footer />
</template>

<script>
import Footer from "@/components/Footer";
import { useStore } from "vuex";
import { computed, ref } from "vue";
import configs from "@/config";

export default {
  components: { Footer },
  setup: () => {
    const store = useStore();

    const isAdmin = computed(() => store.getters["user/isAdmin"]);
    const isGuest = computed(() => store.getters["user/isGuest"]);
    const expanded = ref(false);
    const toggleExpanded = () => (expanded.value = !expanded.value);

    const manual = computed(() => store.getters["config/manual"] ?? "alo");

    return {
      isAdmin,
      isGuest,
      expanded,
      toggleExpanded,
      configs,
      manual,
    };
  },
};
</script>

<style scoped>
#main-content {
  min-height: calc(100vh - 120px);
}

@media screen and (max-width: 1023px) {
  .navbar-brand {
    position: absolute;
    top: 0;
    width: 100%;
  }

  .navbar-menu .navbar-item:first-child {
    margin-left: 8px;
    margin-top: 24px;
  }
}
</style>
