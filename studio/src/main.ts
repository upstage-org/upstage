import { createApp } from "vue";
import App from "./App.vue";
import i18n from "./i18n";
import "./styles/studio.less";
import { router } from "router";
import store from "./store";
import "@fortawesome/fontawesome-free/css/all.css";

createApp(App).use(store).use(router).use(i18n).mount("#app");
