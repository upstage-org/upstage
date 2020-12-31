import { createStore } from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import auth from "./modules/auth";
import user from "./modules/user";
import stage from "./modules/stage";

const dataState = createPersistedState({
  paths: ["auth"],
});

export default createStore({
  modules: {
    auth,
    user,
    stage,
  },
  plugins: [dataState],
})
