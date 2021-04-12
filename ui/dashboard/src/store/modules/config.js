import { configGraph } from "@/services/graphql";

export default {
    namespaced: true,
    state: {
        nginx: {},
        system: {}
    },
    getters: {
        uploadLimit(state) {
            return state.nginx.uploadLimit ?? 1024 * 1024
        },
        termsOfService(state) {
            return state.system.termsOfService
        }
    },
    mutations: {
        STORE_CONFIG(state, configs) {
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
