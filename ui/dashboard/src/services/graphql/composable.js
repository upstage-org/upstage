import store from "@/store";
import { computed, reactive, ref } from "vue";
import hash from 'object-hash';

export const useRequest = (service, ...params) => {
    const loading = ref(false);
    const data = ref();
    const nodes = computed(() => {
        if (!data.value) return null;
        const key = Object.keys(data.value)[0];
        return data.value[key].edges.map((edge) => edge.node)
    });
    const cacheKeys = reactive([]);

    const fetch = async (...newParams) => {
        try {
            const payload = newParams.length ? newParams : params
            const cacheKey = hash({ service, payload });
            const cached = store.state.cache.graphql[cacheKey];
            if (cached) {
                data.value = cached;
            } else {
                loading.value = true;
                data.value = await service(...payload);
                if (data.value) {
                    store.commit('cache/SET_GRAPHQL_CACHE', { key: cacheKey, value: data.value });
                    cacheKeys.push(cacheKey)
                }
            }
            return data.value;
        } catch (error) {
            throw error.response.errors[0].message;
        } finally {
            loading.value = false;
        }
    }

    const clearCache = () => {
        store.commit('cache/CLEAR_GRAPHQL_CACHES', { keys: cacheKeys });
        cacheKeys.length = 0;
    }

    const refresh = (...params) => {
        clearCache();
        return fetch(...params);
    }

    return { loading, data, nodes, fetch, clearCache, refresh }
}

export const useMutation = (...params) => {
    const { fetch, ...rest } = useRequest(...params);
    return { mutation: fetch, ...rest }
};


export const useQuery = (...params) => {
    const { fetch, ...rest } = useRequest(...params);
    fetch();
    return { fetch, ...rest }
};

export const useFirst = (nodes) => {
    return computed(() => (nodes.value && nodes.value.length && nodes.value[0]) ?? {});
}