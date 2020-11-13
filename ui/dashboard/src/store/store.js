import Vue from "vue";
import Vuex from "vuex";
import auth from "./modules/auth";
import user from "./modules/user";
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);

const dataState = createPersistedState({
  paths: ["auth"],
});

export default new Vuex.Store({
  modules: {
    auth,
    user,
  },
  plugins: [dataState],
});
