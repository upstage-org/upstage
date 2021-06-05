
export default {
    namespaced: true,
    state: {
        graphql: {},
    },
    mutations: {
        SET_GRAPHQL_CACHE(state, { key, value }) {
            state.graphql[key] = value;
        },
        CLEAR_GRAPHQL_CACHES(state, { keys }) {
            keys.forEach(key => {
                delete state.graphql[key]
            });
        },
        CLEAR_ALL_GRAPHQL_CACHES(state) {
            Object.keys(state.graphql).forEach(key => {
                delete state.graphql[key]
            });
        }
    },
};
