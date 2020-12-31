import { userService } from "@/services";

export default {
  namespaced: true,
  state: {
    user: null,
    loadingUser: false,
  },
  mutations: {
    SET_USER_DATA(state, data) {
      state.user = data;
    },
    SET_LOADING_USER(state, loading) {
      state.loadingUser = loading;
    },
  },
  actions: {
    fetchCurrent({ commit }) {
      return new Promise((resolve) => {
        commit("SET_LOADING_USER", true);
        userService
          .getCurrent()
          .then((data) => {
            commit("SET_USER_DATA", data);
            resolve();
          })
          .catch((err) => {
            console.log(err)
          })
          .finally(() => {
            commit("SET_LOADING_USER", false);
          });
      });
    },
  },
  getters: {
    currentUser(state) {
      return state.user ? state.user.username : "Annonymous";
    },
  },
};
