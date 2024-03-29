import { message } from "ant-design-vue";
import { createClient } from "genql/studio";
import { getSharedAuth, setSharedAuth } from "utils/common";

let refreshing = false;

export const genqlFetch = async (...params: Parameters<typeof fetch>) => {
  const auth = getSharedAuth();
  if (auth?.token) {
    if (!params[1]) {
      params[1] = {};
    }
    params[1].headers = {
      ...params[1]?.headers,
      "X-Access-Token": auth.token,
    };
  }
  try {
    const response = await fetch(...params);
    const okResponse = response.clone(); // performance check
    const result = await response.json();

    if (!result.errors) {
      return okResponse;
    }

    const errorMessage = result.errors[0].message;
    if (errorMessage === "Signature has expired" && auth?.refresh_token) {
      if (!refreshing) {
        refreshing = true;
        try {
          const refreshTokenClient = createClient({
            headers: {
              "X-Access-Token": auth.refresh_token,
            },
          });
          const { refreshUser } = await refreshTokenClient.mutation({
            refreshUser: {
              __args: {
                refreshToken: auth.refresh_token,
              },
              newToken: true,
            },
          });
          refreshing = false;
          setSharedAuth({
            token: refreshUser?.newToken ?? "",
            refresh_token: auth.refresh_token ?? "",
            username: auth?.username ?? "",
          });

          if (!params[1]) {
            params[1] = {};
          }
          params[1].headers = {
            ...params[1]?.headers,
            "X-Access-Token": refreshUser?.newToken ?? "",
          };
          return fetch(...params);
        } catch (error) {
          message.error(
            `Token expired, could not refresh your access token. Please login again!`,
          );
          return;
        }
      } else {
        await new Promise((res) => setTimeout(res, 1000));
        return fetch(...params);
      }
    } else {
      throw errorMessage;
    }
  } catch (error) {
    if (typeof error === "string") {
      throw error;
    } else {
      message.error(
        "Unknown error! Please check the console log for more information.",
      );
      console.error(error);
    }
  }
};
