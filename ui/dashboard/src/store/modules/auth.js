import { authService } from "@/services";

import {
  setToken,
  removeToken,
  setRefreshToken,
  removeRefreshToken,
} from "@/utils/auth";

export default {
  namespaced: true,
  state: {
    token: "",
    refresh_token: "",
  },
  mutations: {
    SET_TOKEN(state, data) {
      state.token = data;
    },
    SET_REFRESH_TOKEN(state, data) {
      state.refresh_token = data;
    },
    CLEAR_USER_DATA(state) {
      state.token = "";
      state.refresh_token = "";
      location.reload();
    },
  },
  actions: {
    login({ commit }, user) {
      return new Promise((resolve, reject) => {
        authService
          .login(user)
          .then((resp) => {
            if (resp) {
              const { access_token, refresh_token } = resp;
              console.log(refresh_token);
              setToken(access_token);
              setRefreshToken(refresh_token);
              commit("SET_TOKEN", access_token);
              commit("SET_REFRESH_TOKEN", refresh_token);
              resolve();
            }
          })
          .catch((err) => {
            reject(err);
          });
      });
    },
    logout({ commit }) {
      commit("CLEAR_USER_DATA");
      removeToken();
      removeRefreshToken();
    },
    // eslint-disable-next-line no-unused-vars
    fetchRefreshToken({ commit, state }) {
      return new Promise((resolve, reject) => {
        authService
          .getRefreshToken(state.refresh_token)
          .then((resp) => {
            commit("SET_TOKEN", resp);
            resolve();
            return resp;
          })
          .catch((err) => reject(err));
      });
    },
  },
  getters: {
    loggedIn(state) {
      return !!state.token;
    },
    getToken(state) {
      return state.token;
    },
    getRefreshToken(state) {
      return state.refresh_token;
    },
  },
};
