const { APP_CONFIG } = process.env;
const ACCESS_TOKEN_KEY = "access_token";

let appSettings;
try {
  appSettings = JSON.parse(APP_CONFIG || "http://159.89.19.111/V2.0/");
} catch (ex) {
  appSettings = {
    API_ENDPOINT: "http://159.89.19.111/V2.0/",
  };
}

export const baseUrl = new URL(appSettings.API_ENDPOINT).toString();

export const setAccessToken = (accessToken) =>
  localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);

export const clearAccessToken = () => localStorage.removeItem(ACCESS_TOKEN_KEY);
