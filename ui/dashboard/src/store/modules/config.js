import { configGraph } from "@/services/graphql";

export default {
    namespaced: true,
    state: {
        nginx: {},
    },
    getters: {
        uploadLimit(state) {
            return state.nginx.uploadLimit ?? 1024 * 1024
        }
    },
    mutations: {
        STORE_CONFIG(state, configs) {
            console.log
            Object.assign(state, configs)
        },
    },
    actions: {
        async fetchConfig({ commit }) {
            const configs = await configGraph.configs()
            commit('STORE_CONFIG', configs);
        }
    }
};
