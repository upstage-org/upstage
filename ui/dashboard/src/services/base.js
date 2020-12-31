import config from '@/config'

export const baseUrl = new URL(config.API_ENDPOINT).toString();

export const setAccessToken = (accessToken) =>
  localStorage.setItem(config.ACCESS_TOKEN_KEY, accessToken);

export const clearAccessToken = () => localStorage.removeItem(config.ACCESS_TOKEN_KEY);
