import { GraphQLClient } from 'graphql-request';
export { gql } from 'graphql-request';
import config from '@/config';
import store from '@/store/index';
import hash from 'object-hash';

const options = {
    headers: {}
};

export const createClient = namespace => ({
    request: async (...params) => {
        const cacheKey = hash(params);
        const cached = store.state.cache.graphql[cacheKey];
        if (cached) {
            return cached;
        }
        let response = null;
        const client = new GraphQLClient(`${config.GRAPHQL_ENDPOINT}${namespace}/`, options)
        const token = store.getters["auth/getToken"];
        if (token) {
            client.setHeader('X-Access-Token', token)
        }
        try {
            response = await client.request(...params);
        } catch (error) {
            const refreshToken = store.getters["auth/getRefreshToken"]
            if (refreshToken) {
                if (error.response.errors[0].message === 'Signature has expired') { // refresh token
                    const newToken = await store.dispatch("auth/fetchRefreshToken");
                    client.setHeader('X-Access-Token', newToken);
                    response = await client.request(...params);
                }
            } else {
                throw (error);
            }
        }
        if (response) {
            store.commit('cache/SET_GRAPHQL_CACHE', { key: cacheKey, value: response });
        }
        return response;
    }
})