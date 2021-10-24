const { VUE_APP_API_ENDPOINT, VUE_APP_GRAPHQL_ENDPOINT, VUE_APP_STATIC_ASSETS_ENDPOINT, VUE_APP_STUDIO_ENDPOINT, VUE_APP_MQTT_NAMESPACE } = process.env;

let configs = {
    API_ENDPOINT: VUE_APP_API_ENDPOINT,
    GRAPHQL_ENDPOINT: VUE_APP_GRAPHQL_ENDPOINT,
    STATIC_ASSETS_ENDPOINT: VUE_APP_STATIC_ASSETS_ENDPOINT,
    STUDIO_ENDPOINT: VUE_APP_STUDIO_ENDPOINT,
    AXIOS_TIMEOUT: 10000,
    ACCESS_TOKEN_KEY: 'access_token',
    MQTT_NAMESPACE: VUE_APP_MQTT_NAMESPACE,
    MQTT_CONNECTION: {
        url: 'wss://svc1.upstage.org.nz:9002/mqtt',
        username: 'performance',
        password: 'z48FCTsJVEUkYmtUw5S9',
        clean: true, // Reserved session
        connectTimeout: 4000, // Time out
        reconnectPeriod: 4000, // Reconnection interval
        retain: true,
    },
    STREAMING: {
        publish: "rtmp://streaming1.upstage.org.nz:1941/live",
        subscribe: "https://streaming1.upstage.org.nz:9999/",
        auth: {
            username: 'admin',
            password: 'admin'
        }
    }
}

export default configs;
