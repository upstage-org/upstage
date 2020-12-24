import Cookies from "js-cookie";

const ACCESS_TOKEN = "access_token";
const REFRESH_TOKEN = "refresh_token";

export const setToken = (token) => {
  Cookies.set(ACCESS_TOKEN, JSON.stringify(token), { secure: true });
};
export const getToken = () => Cookies.get(ACCESS_TOKEN);
export const removeToken = () => Cookies.remove(ACCESS_TOKEN);

export const setRefreshToken = (token) => Cookies.set(REFRESH_TOKEN, token);
export const getRefreshToken = () => Cookies.get(REFRESH_TOKEN);
export const removeRefreshToken = () => Cookies.remove(REFRESH_TOKEN);
