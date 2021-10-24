import { ApolloClient, createHttpLink, InMemoryCache,makeVar } from '@apollo/client/core'
import configs from './config'

// HTTP connection to the API
const httpLink = createHttpLink({
  // You should use an absolute URL here
  uri: configs.GRAPHQL_ENDPOINT,
})

// Cache implementation
export const inquiryVar = makeVar({})
const cache = new InMemoryCache({
  typePolicies:{
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
  link: httpLink,
  cache,
})