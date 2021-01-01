<template>
  <router-view />
</template>

<script>
import { onMounted } from "vue";
import { useStore } from "vuex";
export default {
  setup: () => {
    onMounted(() => {
      const store = useStore();
      store.dispatch("user/fetchCurrent");
    });
  },
};
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
.is-fullwidth {
  width: 100%;
}
.is-fullheight {
  height: 100%;
}
.clickable {
  pointer-events: all !important;
}
</style>
