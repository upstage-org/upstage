// import { getRefreshToken } from "@/utils/auth";
import { baseUrl } from "./base";
import baseService from "./baseService";

export default {
  async getCurrent() {
    const url = `${baseUrl}logged_in/`;
    const config = {};
    const resp = await baseService.get(url, config);
    const { data } = resp;

    return data || null;
  },
};
