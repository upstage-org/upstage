import axios from "axios";
import store from "@/store/index";
import router from "@/router";
// import router from "@/router";

const AXIOS_TIMEOUT = 10000;

const mockApi = "https://5f3bb099fff8550016ae5862.mockapi.io/api";

const axiosInstance = axios.create({
  baseURL: mockApi,
  timeout: AXIOS_TIMEOUT,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
});

axiosInstance.interceptors.request.use(
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
    console.log("error request", error);

    return Promise.reject(error);
  }
);

axiosInstance.interceptors.response.use(
  (response) => ({ ...response, error: null }),
  (error) => {
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
            return axiosInstance({
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
      // window.location.replace("/login");
      // window.localStorage.clear();
    }

    return Promise.reject(error);
  }
);

export default axiosInstance;
