export default {
    namespaced: true,
    state: {
        background: null,
        status: 'OFFLINE',
    },
    mutations: {
        SET_BACKGROUND(state, background) {
            state.background = background
        },
        SET_STATUS(state, status) {
            state.status = status
        }
    },
    actions: {
        setBackground({ commit }, background) {
            commit('SET_BACKGROUND', background);
        },
        connect({ commit }) {
            commit('SET_STATUS', 'LIVE')
        },
    },
    getters: {
    },
};
