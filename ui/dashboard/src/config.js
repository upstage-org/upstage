const { VUE_APP_CONFIG } = process.env;

let configs = {
    API_ENDPOINT: 'http://159.89.19.111/V4.0/',
    GRAPHQL_ENDPOINT: 'http://159.89.19.111/V4.0/',
    STATIC_ASSETS_ENDPOINT: 'http://159.89.19.111/V4.0/static/assets/',
    AXIOS_TIMEOUT: 10000,
    ACCESS_TOKEN_KEY: 'access_token',
    MQTT_CONNECTION: {
        host: '128.199.117.17',
        port: 9001,
        endpoint: '/mqtt',
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
