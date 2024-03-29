import configs from "config";
import { SharedAuth, SharedConfigs } from "models/config";
import { User as LegacyUser } from "models/studio";
import { User } from "genql/studio";

export function absolutePath(path: string) {
  return `${configs.SHARED?.STATIC_ASSETS_ENDPOINT}${path}`;
}

export function getSharedConfig(): SharedConfigs {
  try {
    const sharedConfig = JSON.parse(localStorage.getItem("configs") ?? "");
    return sharedConfig;
  } catch (error) {
    if (import.meta.env.PROD) {
      localStorage.clear(); // Remove shared auth so that it will ask you to visit Dashboard for login
    }
    return {
      GRAPHQL_ENDPOINT: import.meta.env.VITE_GRAPHQL_ENDPOINT,
      MQTT_CONNECTION: {},
      STREAMING: {
        auth: {},
      },
    } as SharedConfigs;
  }
}

export function getSharedAuth(): SharedAuth | undefined {
  try {
    const sharedStateJSON = localStorage.getItem("vuex");
    if (sharedStateJSON) {
      const sharedState = JSON.parse(sharedStateJSON);
      return sharedState.auth;
    }
  } catch (error) {
    console.log("No shared auth found. Try login using dashboard first!");
  }
}

export function setSharedAuth(auth: SharedAuth) {
  const vuex = JSON.parse(localStorage.getItem("vuex") || "{}");
  localStorage.setItem("vuex", JSON.stringify({ ...vuex, auth }));
}

export function humanFileSize(bytes: number, si = false, dp = 1) {
  const thresh = si ? 1000 : 1024;

  if (Math.abs(bytes) < thresh) {
    return bytes + " B";
  }

  const units = ["kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];
  let u = -1;
  const r = 10 ** dp;

  do {
    bytes /= thresh;
    ++u;
  } while (
    Math.round(Math.abs(bytes) * r) / r >= thresh &&
    u < units.length - 1
  );

  return bytes.toFixed(dp) + " " + units[u];
}

export function capitalize(str: string) {
  return str ? str.charAt(0).toUpperCase() + str.slice(1) : "";
}

export function titleCase(str: string) {
  if (!str) {
    return "";
  }
  var splitStr = str.toLowerCase().replace(/_/g, " ").split(" ");
  for (var i = 0; i < splitStr.length; i++) {
    splitStr[i] =
      splitStr[i].charAt(0).toUpperCase() + splitStr[i].substring(1);
  }
  return splitStr.join(" ");
}

export function displayName(
  user: Pick<
    User | LegacyUser,
    "displayName" | "firstName" | "lastName" | "username"
  >,
) {
  if (user.displayName?.trim()) return user.displayName;
  if (user.firstName || user.lastName)
    return `${user.firstName ?? ""} ${user.lastName ?? ""}`.trim();
  return user.username;
}
