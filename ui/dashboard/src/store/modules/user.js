import { userService } from "@/services";

export default {
  namespaced: true,
  state: {
    user: null,
    loadingUser: false,
    nickname: null,
    avatarId: null,
  },
  mutations: {
    SET_USER_DATA(state, data) {
      state.user = data;
    },
    SET_LOADING_USER(state, loading) {
      state.loadingUser = loading;
    },
    SET_NICK_NAME(state, nickname) {
      state.nickname = nickname;
    },
    SET_AVATAR_ID(state, id) {
      state.avatarId = id;
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
    saveNickname({ commit }, { nickname }) {
      commit('SET_NICK_NAME', nickname);
      return nickname;
    },
    setAvatarId({ commit }, { name, id }) {
      commit('SET_NICK_NAME', name);
      commit('SET_AVATAR_ID', id);
    }
  },
  getters: {
    nickname(state) {
      return state.nickname ?? (state.user ? (state.user.firstname ?? state.user.username) : "Guest");
    },
  },
};
