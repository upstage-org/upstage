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
        if (['Missing X-Access-Token Header', 'Signature verification failed', 'Signature has expired'].some(message => error.message?.includes(message))) {
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
    async saveNickname({ commit, state, dispatch, getters }, { nickname }) {
      const avatar = getters.avatar
      if (avatar) {
        dispatch("stage/shapeObject", {
          ...avatar,
          name: nickname,
        }, { root: true });
      } else {
        commit('SET_NICK_NAME', nickname);
        dispatch('stage/joinStage', null, { root: true });
        if (state.user && state.user.id) {
          const response = await userGraph.updateUser({
            ...state.user,
            displayName: nickname
          });
          return response.updateUser.user.displayName;
        }
      }
      return nickname;
    },
    setAvatarId({ commit, dispatch }, id) {
      commit('SET_AVATAR_ID', id);
      dispatch('stage/joinStage', null, { root: true });
    },
  },
  getters: {
    nickname(state) {
      return state.nickname ?? (state.user ? displayName(state.user) : "Guest");
    },
    chatname(state, getters) {
      let name = getters.nickname;
      const avatar = getters.avatar
      if (avatar && avatar.name) {
        name = avatar.name
      }
      return name;
    },
    isAdmin(state) {
      return [ROLES.ADMIN, ROLES.SUPER_ADMIN].includes(state.user?.role);
    },
    avatarId(state) {
      return state.avatarId;
    },
    avatar(state, getters, rootState) {
      if (state.avatarId) {
        const avatar = rootState.stage.board.objects.find(o => o.id === state.avatarId);
        return avatar;
      }
    }
  },
};
