import { computed, ref } from "vue";
import { notification } from "@/utils/notification";

export const useRequest = (service, ...params) => {
    const loading = ref(false);
    const data = ref();
    const nodes = computed(() => {
        if (!data.value) return null;
        const key = Object.keys(data.value)[0];
        return data.value[key].edges.map((edge) => edge.node)
    });
    const fetch = async () => {
        try {
            loading.value = true;
            data.value = await service(...params);
        } catch (error) {
            notification.error(error.response.errors[0].message);
        } finally {
            loading.value = false;
        }
    }

    return { loading, data, nodes, fetch }
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