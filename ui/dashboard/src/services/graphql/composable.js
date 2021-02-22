import { ref } from "vue";
import { notification } from "@/utils/notification";

export const useQuery = (service, immediate, ...params) => {
    const loading = ref(false);
    const data = ref();
    const fetch = async () => {
        try {
            loading.value = true;
            data.value = await service(...params);
        } catch (error) {
            notification.error(error);
        } finally {
            loading.value = false;
        }
    }
    if (immediate) {
        fetch();
    }

    return { loading, data, fetch }
}

export const useMutation = useQuery;