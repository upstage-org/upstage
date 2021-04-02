import router from '@/router';
import { userGraph } from '@/services/graphql';
import { displayName, logout } from '@/utils/auth';
import { ROLES } from '@/utils/constants';
import { notification } from '@/utils/notification';

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
        const { currentUser } = await userGraph.currentUser();
        commit("SET_USER_DATA", currentUser);
        return currentUser;
      } catch (error) {
        if (['Missing X-Access-Token Header', 'Signature verification failed'].some(message => error.message?.includes(message))) {
          logout();

          if (router.currentRoute.value.meta.requireAuth) {
            router.push("/login");
            notification.warning('You have been logged out of this session!');
          }
        }
      } finally {
        commit("SET_LOADING_USER", false);
      }
    },
    async saveNickname({ commit, state, dispatch }, { nickname }) {
      commit('SET_NICK_NAME', nickname);
      try {
        const response = await userGraph.updateUser({
          ...state.user,
          displayName: nickname
        });
        dispatch('stage/joinStage', null, { root: true });
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
      return state.nickname ?? (state.user ? displayName(state.user) : "Guest");
    },
    isAdmin(state) {
      return [ROLES.ADMIN, ROLES.SUPER_ADMIN].includes(state.user?.role);
    },
  },
};
