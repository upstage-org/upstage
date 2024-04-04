<script setup lang="ts">
import { apolloClient } from "apollo";
import { provide, onMounted } from "vue";
import { DefaultApolloClient } from "@vue/apollo-composable";
import "styles/bulma.css";
import "styles/custom.less";
import { useStore } from "vuex";


provide(DefaultApolloClient, apolloClient);

const store = useStore();
store.dispatch("user/fetchCurrent");
store.dispatch("config/fetchConfig");
onMounted(() => {
  caches.keys().then((keyList) => {
    Promise.all(keyList.map((key) => caches.delete(key)))
  })
});

</script>

<template>
  <a-config-provider :theme="{
    token: {
      colorPrimary: '#007011',
      borderRadius: 4,
      fontSize: 16,
      fontFamily: 'Josefin Sans, sans-serif',
      colorPrimaryBg: '#ffffff',
    },
    components: {},
  }">
    <router-view />
  </a-config-provider>
</template>
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

@media screen and (max-width: 768px) {
  .is-fullwidth-mobile {
    width: 100%;
  }
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

.root {
  padding: 0px !important;
}
</style>