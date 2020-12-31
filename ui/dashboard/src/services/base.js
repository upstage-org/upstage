import axios from "axios";
import store from "@/store/index";
import router from "@/router";
import { notification } from "@/utils/notification";
import config from '../config';

const baseURL = new URL(config.API_ENDPOINT).toString();

axios.defaults.baseURL = baseURL;
axios.defaults.timeout = config.AXIOS_TIMEOUT;
axios.defaults.headers.common = {
  Accept: "application/json",
  "Content-Type": "application/json",
}

const requestInterceptor = axios.interceptors.request.use(
  (config) => {
    // do something before request is sent
    const token = store.getters["auth/getToken"] || "";

    if (token && typeof config.headers["X-Access-Token"] === "undefined") {
      config.headers["X-Access-Token"] = token;
    }

    config.headers["Accept"] = "application/json";

    config.headers["Content-Type"] = "application/json";

    config.headers["Access-Control-Allow-Origin"] = "*";

    return config;
  },

  (error) => {
    return Promise.reject(error);
  }
);

const responseInterceptor = axios.interceptors.response.use(
  (response) => ({ ...response, error: null }),
  (error) => {
    const message = error?.response?.data?.error;
    if (message) {
      notification.error(message)
    }
    const token = store.getters["auth/getToken"] || "";

    if (
      error?.response?.status === 401 ||
      (error?.response?.status && token && token.length > 0)
    ) {
      const originalRequest = error.config;
      if (originalRequest.url.indexOf("access_token/refresh") > 0) {
        router.push("/login");
        return Promise.reject(error);
      }
      if (!originalRequest._retry) {
        return store
          .dispatch("auth/fetchRefreshToken")
          .then((resp) => {
            originalRequest._retry = true;
            return axios.create({
              url: originalRequest.url,
              method: originalRequest.method,
              headers: {
                Accept: originalRequest.headers.Accept,
                "X-Access-Token": resp,
              },
            });
          })
          .catch(() => {
            router.push("/login");
          });
      }
    }

    return Promise.reject(error);
  }
);

const extend = (customize) => {
  const instance = axios.create();
  instance.interceptors.request.handlers = axios.interceptors.request.handlers;
  instance.interceptors.response.handlers = axios.interceptors.response.handlers;
  if (customize) {
    customize(instance);
  }
  return instance;
}

export { baseURL, requestInterceptor, responseInterceptor, extend }