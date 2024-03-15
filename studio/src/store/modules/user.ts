// @ts-nocheck
import { displayName } from "utils/common";
import { ROLES } from "utils/constants";

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
      
    },
    async saveNickname({ commit, dispatch, getters }, { nickname }) {
      const avatar = getters.avatar;
      if (avatar) {
        dispatch(
          "stage/shapeObject",
          {
            ...avatar,
            name: nickname,
          },
          { root: true },
        );
      } else {
        commit("SET_NICK_NAME", nickname);
        dispatch("stage/joinStage", null, { root: true });
      }
      return nickname;
    },
    setAvatarId({ commit, dispatch }, id) {
      commit("SET_AVATAR_ID", id);
      dispatch("stage/joinStage", null, { root: true });
    },
    async checkIsAdmin({ commit }) {
      commit("SET_LOADING_USER", true);
      // try {
      //   const { currentUser } = await userGraph.currentUser();
      //   return [ROLES.ADMIN, ROLES.SUPER_ADMIN].includes(currentUser?.role);
      // } catch (error) {
      //   if (
      //     [
      //       "Missing X-Access-Token Header",
      //       "Signature verification failed",
      //       "Signature has expired",
      //     ].some((message) => error.message?.includes(message))
      //   ) {
      //     //logout();

      //     // if (router.currentRoute.value.meta.requireAuth) {
      //     //   router.push("/login");
      //     //   notification.warning("You have been logged out of this session!");
      //     // }
      //   }
      // } finally {
      //   commit("SET_LOADING_USER", false);
      // }
    },
    async checkIsGuest({ commit }) {
      commit("SET_LOADING_USER", true);
      // try {
      //   const { currentUser } = await userGraph.currentUser();
      //   if (!currentUser) {
      //     return true;
      //   }
      //   if (currentUser.role === ROLES.GUEST) {
      //     return true;
      //   }
      //   return false;
      // } catch (error) {
      //   if (
      //     [
      //       "Missing X-Access-Token Header",
      //       "Signature verification failed",
      //       "Signature has expired",
      //     ].some((message) => error.message?.includes(message))
      //   ) {
      //     logout();

      //     // if (router.currentRoute.value.meta.requireAuth) {
      //     //   router.push("/login");
      //     //   notification.warning("You have been logged out of this session!");
      //     // }
      //   }
      // } finally {
      //   commit("SET_LOADING_USER", false);
      // }
    },
  },
  getters: {
    nickname(state) {
      return state.nickname ?? (state.user ? displayName(state.user) : "Guest");
    },
    chatname(state, getters) {
      let name = getters.nickname;
      const avatar = getters.avatar;
      if (avatar && avatar.name) {
        name = avatar.name;
      }
      return name;
    },
    isAdmin(state) {
      return [ROLES.ADMIN, ROLES.SUPER_ADMIN].includes(state.user?.role);
    },
    isGuest(state) {
      if (!state.user) {
        return true;
      }
      if (state.user.role === ROLES.GUEST) {
        return true;
      }
      return false;
    },
    avatarId(state) {
      return state.avatarId;
    },
    avatar(state, getters, rootState) {
      if (state.avatarId) {
        const avatar = rootState.stage.board.objects.find(
          (o) => o.id === state.avatarId,
        );
        return avatar;
      }
    },
    currentUserId(state) {
      return state.user.id;
    },
  },
};
