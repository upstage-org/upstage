import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";
import auth from "./modules/auth";
import user from "./modules/user";
import stage from "./modules/stage";
import cache from "./modules/cache";
import config from "./modules/config";

const dataState = createPersistedState({
  paths: ["auth"],
});

export default createStore({
  modules: {
    auth,
    user,
    stage,
    cache,
    config,
  },
  plugins: [dataState],
});
