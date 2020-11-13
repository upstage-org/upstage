// import { getRefreshToken } from "@/utils/auth";
import { baseUrl } from "./base";
import baseService from "./baseService";
import axios from "axios";

export default {
  async login(user) {
    const url = `${baseUrl}access_token/`;
    const config = {};
    const resp = await baseService.post(url, user, config);
    const { data } = resp;

    return data || null;
  },
  async getRefreshToken(refreshToken) {
    const url = `${baseUrl}access_token/refresh/`;
    const instance = axios.create({
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        "X-Access-Token": refreshToken,
      },
    });
    const resp = await instance.post(url);
    const { data } = resp;

    return (data && data["access_token"]) || null;
  },
  async getCurrent() {
    const url = `${baseUrl}logged_in/`;
    const config = {};
    const resp = await baseService.get(url, config);
    const { data } = resp;

    return data || null;
  },
};
