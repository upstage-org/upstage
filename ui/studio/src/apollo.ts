import { ApolloClient, createHttpLink, InMemoryCache, makeVar, from, fromPromise } from '@apollo/client/core'
import { setContext } from '@apollo/client/link/context';
import { onError } from "@apollo/client/link/error";
import { message } from 'ant-design-vue';
import configs from './config'
import { getSharedAuth, setSharedAuth } from './utils/common';
import gql from 'graphql-tag';
import { Media } from './models/studio';

// HTTP connection to the API
const httpLink = createHttpLink({
  // You should use an absolute URL here
  uri: configs.GRAPHQL_ENDPOINT,
})

let refreshing = false

const errorLink = onError(({ graphQLErrors, networkError, operation, forward }) => {
  if (graphQLErrors) {
    for (let err of graphQLErrors) {
      const refreshToken = getSharedAuth()?.refresh_token

      if (err.message === 'Signature has expired') {
        if (!refreshing) {
          refreshing = true
          return fromPromise(
            apolloClient.mutate({
              mutation: gql`
              mutation refreshUser($refreshToken: String) {
                refreshUser(refreshToken: $refreshToken) {
                  newToken
                }
              }
            `,
              context: {
                headers: {
                  'X-Access-Token': refreshToken
                }
              },
              variables: {
                refreshToken
              }
            }).catch(() => {
              // Handle token refresh errors e.g clear stored tokens, redirect to login
              message.error(`Token expired, could not refresh your access token. Please login again!`);
              return;
            })
          ).map((value) => value?.data.refreshUser.newToken)
            .filter((value) => Boolean(value))
            .flatMap((accessToken) => {
              refreshing = false
              setSharedAuth({
                token: accessToken,
                refresh_token: refreshToken ?? ''
              })
              // modify the operation context with a new token
              operation.setContext({
                headers: {
                  ...operation.getContext().headers,
                  'X-Access-Token': accessToken,
                },
              });
              return forward(operation);
            });
        } else {
          return fromPromise(new Promise((resolve) => {
            const loop = () => {
              if (!refreshing) {
                resolve(getSharedAuth()?.token)
              } else {
                setTimeout(loop, 500)
              }
            }
            loop()
          }
          )).flatMap((accessToken) => {
            operation.setContext({
              headers: {
                ...operation.getContext().headers,
                'X-Access-Token': accessToken,
              },
            });
            return forward(operation);
          })
        }
      }
    }
  }
  if (networkError) message.error(`[Network error]: ${networkError}`);
});

const authLink = setContext((request, { headers }) => {
  // get the authentication token from local storage if it exists
  const auth = getSharedAuth()
  // return the headers to the context so httpLink can read them
  return {
    headers: {
      'X-Access-Token': auth?.token,
      ...headers,
    }
  }
});

// Cache implementation
export const inquiryVar = makeVar({})
export const editingMediaVar = makeVar<Media | undefined>(undefined)
const cache = new InMemoryCache({
  typePolicies: {
    Query: {
      fields: {
        inquiry: {
          read() {
            return inquiryVar()
          }
        },
        editingMedia: {
          read() {
            return editingMediaVar()
          }
        }
      }
    }
  }
})

// Create the apollo client
export const apolloClient = new ApolloClient({
  link: from([errorLink, authLink, httpLink]),
  cache,
})