import { ApolloClient, createHttpLink, InMemoryCache, makeVar } from '@apollo/client/core'
import { setContext } from '@apollo/client/link/context';
import configs from './config'
import { getSharedAuth } from './utils/common';

// HTTP connection to the API
const httpLink = createHttpLink({
  // You should use an absolute URL here
  uri: configs.GRAPHQL_ENDPOINT,
})

const authLink = setContext((_, { headers }) => {
  // get the authentication token from local storage if it exists
  const auth = getSharedAuth()
  // return the headers to the context so httpLink can read them
  return {
    headers: {
      ...headers,
      'X-Access-Token': auth?.token,
    }
  }
});

// Cache implementation
export const inquiryVar = makeVar({})
const cache = new InMemoryCache({
  typePolicies: {
    Query: {
      fields: {
        inquiry: {
          read() {
            return inquiryVar()
          }
        }
      }
    }
  }
})

// Create the apollo client
export const apolloClient = new ApolloClient({
  link: authLink.concat(httpLink),
  cache,
})