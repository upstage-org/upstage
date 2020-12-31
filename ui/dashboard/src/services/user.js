import { extend, responseInterceptor } from "./base";

export default {
  async getCurrent() {
    const url = 'logged_in/';
    const config = {};
    const resp = await extend(axios => axios.interceptors.response.eject(responseInterceptor))
      .get(url, config);
    const { data } = resp;

    return data || null;
  },
};
