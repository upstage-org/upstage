import { GraphQLClient } from 'graphql-request';
export { gql } from 'graphql-request';
import config from '@/config';
import store from "@/store/index";


const options = { headers: {} };

export const createClient = namespace => ({
    request: (...params) => {
        const client = new GraphQLClient(`${config.GRAPHQL_ENDPOINT}${namespace}/`, options)
        const token = store.getters["auth/getToken"] || "";
        if (token) {
            client.setHeader('X-Access-Token', token)
        }
        return client.request(...params)
    }
})