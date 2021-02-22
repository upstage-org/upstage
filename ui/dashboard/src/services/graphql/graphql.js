import { GraphQLClient } from 'graphql-request';
export { gql } from 'graphql-request';
import config from '@/config';

const options = { headers: {} };

export const createClient = namespace => new GraphQLClient(`${config.GRAPHQL_ENDPOINT}${namespace}/`, options)
