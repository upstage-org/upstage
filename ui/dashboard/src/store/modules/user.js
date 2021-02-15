import { userService } from "@/services";
import { userGraph, gql } from '@/services/graphql';

export default {
  namespaced: true,
  state: {
    user: null,
    loadingUser: false,
    nickname: null,
    avatarId: null,
    userList: null
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
    SET_USER_LIST(state, users) {
      state.userList = users;
    }
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
    },
    async getUserList({ commit }) {
      const users = await userGraph.request(
        gql`
          {
            userList {
              edges {
                node {
                  id
                  username
                  firstName
                  role
                  email
                  displayName
                }
              }
            }
          }
        `);
      commit('SET_USER_LIST', users);
    }
  },
  getters: {
    nickname(state) {
      return state.nickname ?? (state.user ? (state.user.firstname ?? state.user.username) : "Guest");
    },
  },
};
