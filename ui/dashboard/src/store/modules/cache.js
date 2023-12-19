import { stageGraph } from "@/services/graphql";
import { useRequest } from "@/services/graphql/composable";

export default {
    namespaced: true,
    state: {
        graphql: {},
        stageList: null
    },
    getters: {
        loadingStages(state) {
            return state.stageList === null
        },
        visibleStages(state) {
            return state.stageList ? state.stageList.filter(s => s.visibility) : []
        },
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
        },
        SET_STAGE_LIST(state, list) {
            state.stageList = list
        },
        UPDATE_STAGE_VISIBILITY(state, { stageId, visibility }) {
            const stage = state.stageList.find(s => s.id === stageId);
            if (stage) {
                stage.visibility = visibility;
            }
        }
    },
    actions: {
        async fetchStages({ commit }) {
            try {
                commit('SET_STAGE_LIST', null)
                const { nodes, refresh } = useRequest(stageGraph.stageList);
                await refresh()
                if (nodes.value) {
                    nodes.value.forEach(node => {
                        node.attributes.forEach(attr => node[attr.name] = attr.description)
                    })
                }
                commit('SET_STAGE_LIST', nodes)
            } catch {
                commit('SET_STAGE_LIST', [])
            }
        }
    }
};
