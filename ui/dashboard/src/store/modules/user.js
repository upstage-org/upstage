import { userService } from "@/services";

export default {
  namespaced: true,
  state: {
    user: null,
  },
  mutations: {
    SET_USER_DATA(state, data) {
      state.user = data;
    },
  },
  actions: {
    fetchCurrent({ commit }) {
      return new Promise((resolve, reject) => {
        userService
          .getCurrent()
          .then((resp) => {
            commit("SET_USER_DATA", resp);
            resolve();
          })
          .catch((err) => reject(err));
      });
    },
  },
  getters: {
    currentUser(state) {
      return state.user ? state.user.username : "";
    },
  },
};
