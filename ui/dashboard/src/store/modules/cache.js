
export default {
    namespaced: true,
    state: {
        graphql: {},
    },
    mutations: {
        SET_GRAPHQL_CACHE(state, { key, value }) {
            state.graphql[key] = value;
        },
    },
};
