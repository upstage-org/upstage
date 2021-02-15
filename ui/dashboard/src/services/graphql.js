import { GraphQLClient } from 'graphql-request';
import config from '../config';

export const client = new GraphQLClient(config.GRAPHQL_ENDPOINT, { headers: {} })
