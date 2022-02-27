import { configGraph } from "@/services/graphql";

export default {
    namespaced: true,
    state: {
        nginx: {},
        system: {},
        foyer: null
    },
    getters: {
        uploadLimit(state) {
            return state.nginx.uploadLimit ?? 1024 * 1024
        },
        termsOfService(state) {
            return state.system.termsOfService
        },
        manual(state) {
            return state.system.manual
        },
        foyer(state) {
            return state.foyer ?? {}
        },
        navigations(state) {
            if (!state.foyer) {
                return []
            }
            try {
                const lines = state.foyer.menu.split("\n").filter(line => line.trim().length > 0)
                const navigations = []
                for (const line of lines) {
                    // Syntax: <title> (<url>)
                    const url = line.match(/\(([^)]+)\)/) // get the url part
                    let title = line.replace('>', '')
                    title = title.includes("(") ? title.split("(")[0].trim() : title.trim() // get the title part
                    const menu = { title, url: url ? url[1] : null }
                    if (line.trim().startsWith(">")) {
                        const parent = navigations[navigations.length - 1]
                        if (!parent.children) {
                            parent.children = []
                        }
                        parent.children.push(menu)
                    } else {
                        navigations.push(menu)
                    }
                }
                return navigations
            } catch (error) {
                console.log(error)
            }
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
