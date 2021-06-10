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
      store.dispatch("config/fetchConfig");
      store.dispatch("cache/fetchStages");
    });
  },
};
</script>

<style lang="scss">
html {
  overflow-y: auto !important;
}
body.waiting * {
  cursor: wait !important;
}
.is-fullwidth {
  width: 100%;
}
.is-fullheight {
  height: 100%;
}
.clickable {
  pointer-events: all !important;
  cursor: pointer;
}
[contenteditable] {
  -webkit-user-select: text !important;
  user-select: text !important;
  * {
    font-family: inherit;
  }
}
</style>
