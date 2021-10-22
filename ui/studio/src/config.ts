const configs = {
  MODE: import.meta.env.MODE as 'development' | 'production',
  BACKSTAGE_URL: import.meta.env.VITE_APP_BACKSTAGE_URL as string,
  GRAPHQL_ENDPOINT: import.meta.env.VITE_APP_GRAPHQL_ENDPOINT as string
}

export default configs