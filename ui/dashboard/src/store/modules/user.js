import { userGraph } from '@/services/graphql';

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
    async fetchCurrent({ commit }) {
      commit("SET_LOADING_USER", true);
      try {
        const data = await userGraph.loggedIn();
        commit("SET_USER_DATA", data);
        return data;
      } finally {
        commit("SET_LOADING_USER", false);
      }
    },
    async saveNickname({ commit, state }, { nickname }) {
      commit('SET_NICK_NAME', nickname);
      try {
        const response = await userGraph.updateUser({
          id: state.user.id,
          displayName: nickname
        });
        return response.updateUser.user.displayName;
      } catch (error) {
        return nickname;
      }
    },
    setAvatarId({ commit }, { name, id }) {
      commit('SET_NICK_NAME', name);
      commit('SET_AVATAR_ID', id);
    },
  },
  getters: {
    nickname(state) {
      return state.nickname ?? (state.user ? (state.user.firstname ?? state.user.username) : "Guest");
    },
  },
};
