export default {
    namespaced: true,
    state: {
        background: null,
    },
    mutations: {
        SET_BACKGROUND(state, background) {
            state.background = background
        },
    },
    actions: {
        setBackground({ commit }, background) {
            commit("SET_BACKGROUND", background);
        }
    },
    getters: {
    },
};
