import axios from "axios";

export default {
  async login(user) {
    const url = `access_token/`;
    const config = {};
    const resp = await axios.post(url, user, config);
    const { data } = resp;

    return data || null;
  },
  async getRefreshToken(refreshToken) {
    const url = `access_token/refresh/`;
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
};
