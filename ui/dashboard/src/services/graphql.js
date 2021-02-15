import { GraphQLClient } from 'graphql-request';
export { gql } from 'graphql-request';
import config from '../config';

const options = { headers: {} };

export const userGraph = new GraphQLClient(`${config.GRAPHQL_ENDPOINT}user_graphql/`, options)

export const performanceGraph = new GraphQLClient(`${config.GRAPHQL_ENDPOINT}performance_graphql/`, options)
