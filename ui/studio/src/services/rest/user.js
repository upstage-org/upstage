import { extend } from "./base";

export default {
  async getCurrent() {
    const url = 'logged_in/';
    const config = {};
    const resp = await extend({ hideNotification: true }).get(url, config);
    const { data } = resp;

    return data || null;
  },
};
