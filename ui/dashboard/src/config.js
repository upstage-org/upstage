const { VUE_APP_CONFIG } = process.env;

let configs = {
    API_ENDPOINT: 'https://app1.upstage.org.nz/V4.0/',
    GRAPHQL_ENDPOINT: 'https://app1.upstage.org.nz/V4.0/',
    STATIC_ASSETS_ENDPOINT: 'https://app1.upstage.org.nz/V4.0/static/assets/',
    AXIOS_TIMEOUT: 10000,
    ACCESS_TOKEN_KEY: 'access_token',
    MQTT_CONNECTION: {
        url: 'wss://svc.upstage.org.nz:9001/mqtt',
        username: 'performance',
        password: 'z48FCTsJVEUkYmtUw5S9',
        clean: true, // Reserved session
        connectTimeout: 4000, // Time out
        reconnectPeriod: 4000, // Reconnection interval
        retain: true,
    },
}

if (VUE_APP_CONFIG) {
    const envConfig = JSON.parse(VUE_APP_CONFIG);
    configs = {
        ...configs,
        ...envConfig
    }
}

export default configs;
