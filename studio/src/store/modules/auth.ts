// @ts-nocheck
import { userGraph } from "services/graphql";
import { authService } from "services/rest";

import {
  setToken,
  removeToken,
  setRefreshToken,
  removeRefreshToken,
} from "utils/auth";

export default {
  namespaced: true,
  state: {
    username: "",
    token: "",
    refresh_token: "",
  },
  mutations: {
    SET_USERNAME(state, data) {
      state.username = data;
    },
    SET_TOKEN(state, data) {
      state.token = data;
    },
    SET_REFRESH_TOKEN(state, data) {
      state.refresh_token = data;
    },
    CLEAR_USER_DATA(state) {
      state.token = "";
      state.refresh_token = "";
    },
  },
  actions: {
    login({ commit }, user) {
      return new Promise((resolve, reject) => {
        authService
          .login(user)
          .then(async (resp) => {
            if (resp) {
              const { access_token, refresh_token } = resp;
              setToken(access_token);
              setRefreshToken(refresh_token);
              commit("SET_USERNAME", user.username);
              commit("SET_TOKEN", access_token);
              commit("SET_REFRESH_TOKEN", refresh_token);
              //              await dispatch("user/fetchCurrent", null, { root: true });
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
      localStorage.clear();
      removeToken();
      removeRefreshToken();
    },
    // eslint-disable-next-line no-unused-vars
    fetchRefreshToken({ commit, state }) {
      return userGraph
        .refreshUser(
          {
            refreshToken: state.refresh_token,
          },
          {
            "X-Access-Token": state.refresh_token,
          },
        )
        .then((response) => {
          const token = response.refreshUser.newToken;
          commit("SET_TOKEN", token);
          return token;
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
